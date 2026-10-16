#!/usr/bin/env python3
import argparse
import contextlib
import difflib
import json
import logging
import os
import re
import sys
import types
from collections import Counter
from typing import Any, Dict, List, Optional

# Some environments ship an OpenSSL/pyopenssl combo that breaks requests import.
# Provide a no-op stub to bypass pyopenssl injection if present.
dummy_pyopenssl = types.ModuleType("urllib3.contrib.pyopenssl")
dummy_pyopenssl.inject_into_urllib3 = lambda: None
sys.modules.setdefault("urllib3.contrib.pyopenssl", dummy_pyopenssl)

import requests

logger = logging.getLogger("dblp_cli")

REQUEST_TIMEOUT = 10  # seconds
HEADERS = {
    "User-Agent": "codex-dblp-skill/1.0 (https://github.com/szeider/mcp-dblp)",
    "Accept": "application/json",
}

STATE_DIR = os.path.expanduser("~/.codex/dblp-skill")
STATE_PATH = os.path.join(STATE_DIR, "state.json")


def _load_state() -> Dict[str, Any]:
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(STATE_PATH):
        return {"entries": {}}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_state(state: Dict[str, Any]) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _fetch_publications(single_query: str, max_results: int) -> List[Dict[str, Any]]:
    results = []
    try:
        url = "https://dblp.org/search/publ/api"
        params = {"q": single_query, "format": "json", "h": max_results}
        response = requests.get(url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        hits = data.get("result", {}).get("hits", {})
        total = int(hits.get("@total", "0"))
        logger.info("Found %s results for query: %s", total, single_query)
        if total > 0:
            publications = hits.get("hit", [])
            if not isinstance(publications, list):
                publications = [publications]
            for pub in publications:
                info = pub.get("info", {})
                authors = []
                authors_data = info.get("authors", {}).get("author", [])
                if not isinstance(authors_data, list):
                    authors_data = [authors_data]
                for author in authors_data:
                    if isinstance(author, dict):
                        authors.append(author.get("text", ""))
                    else:
                        authors.append(str(author))

                dblp_url = info.get("url", "")
                if dblp_url:
                    dblp_key = dblp_url.replace("https://dblp.org/rec/", "")
                elif "key" in pub:
                    dblp_key = pub.get("key", "").replace("dblp:", "")
                else:
                    dblp_key = pub.get("@id", "").replace("dblp:", "")

                results.append(
                    {
                        "title": info.get("title", ""),
                        "authors": authors,
                        "venue": info.get("venue", ""),
                        "year": int(info.get("year", 0)) if info.get("year") else None,
                        "type": info.get("type", ""),
                        "doi": info.get("doi", ""),
                        "ee": info.get("ee", ""),
                        "url": info.get("url", ""),
                        "dblp_key": dblp_key,
                    }
                )
    except requests.exceptions.Timeout:
        timeout_msg = f"ERROR: Query '{single_query}' timed out after {REQUEST_TIMEOUT} seconds"
        results.append({"title": timeout_msg, "authors": [], "venue": "Error", "year": None})
    except Exception as e:
        error_msg = f"ERROR: DBLP API error for query '{single_query}': {e}"
        results.append({"title": error_msg, "authors": [], "venue": "Error", "year": None})
    return results


def search(
    query: str,
    max_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    venue_filter: Optional[str] = None,
    include_bibtex: bool = False,
    ) -> List[Dict[str, Any]]:
    query_lower = query.lower()
    results: List[Dict[str, Any]] = []
    if " or " in query_lower:
        subqueries = [q.strip() for q in query_lower.split(" or ") if q.strip()]
        seen = set()
        for q in subqueries:
            for pub in _fetch_publications(q, max_results):
                identifier = (pub.get("title"), pub.get("year"))
                if identifier not in seen:
                    results.append(pub)
                    seen.add(identifier)
    else:
        results = _fetch_publications(query, max_results)

    filtered_results = []
    for result in results:
        if year_from or year_to:
            year = result.get("year")
            if year:
                with contextlib.suppress(ValueError, TypeError):
                    year_int = int(year)
                    if (year_from and year_int < year_from) or (year_to and year_int > year_to):
                        continue
        if venue_filter:
            venue = result.get("venue", "")
            if venue_filter.lower() not in venue.lower():
                continue
        filtered_results.append(result)

    filtered_results = filtered_results[:max_results]

    if include_bibtex:
        for result in filtered_results:
            if result.get("dblp_key"):
                result["bibtex"] = fetch_bibtex_entry(result["dblp_key"])

    return filtered_results


def get_author_publications(
    author_name: str,
    similarity_threshold: float,
    max_results: int = 20,
    include_bibtex: bool = False,
    ) -> Dict[str, Any]:
    author_query = f"author:{author_name}"
    publications = search(author_query, max_results=max_results * 2)

    filtered_publications = []
    for pub in publications:
        best_ratio = 0.0
        for candidate in pub.get("authors", []):
            ratio = difflib.SequenceMatcher(None, author_name.lower(), candidate.lower()).ratio()
            best_ratio = max(best_ratio, ratio)
        if best_ratio >= similarity_threshold:
            filtered_publications.append(pub)

    filtered_publications = filtered_publications[:max_results]

    if include_bibtex:
        for pub in filtered_publications:
            if pub.get("dblp_key"):
                pub["bibtex"] = fetch_bibtex_entry(pub["dblp_key"])

    venues = Counter([p.get("venue", "") for p in filtered_publications])
    years = Counter([p.get("year", "") for p in filtered_publications])
    types = Counter([p.get("type", "") for p in filtered_publications])

    return {
        "name": author_name,
        "publication_count": len(filtered_publications),
        "publications": filtered_publications,
        "stats": {
            "venues": venues.most_common(5),
            "years": years.most_common(5),
            "types": dict(types),
        },
    }


def fuzzy_title_search(
    title: str,
    similarity_threshold: float,
    max_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    venue_filter: Optional[str] = None,
    include_bibtex: bool = False,
    ) -> List[Dict[str, Any]]:
    candidates = []
    seen_titles = set()

    title_query = f"title:{title}"
    results = search(
        title_query,
        max_results=max_results * 3,
        year_from=year_from,
        year_to=year_to,
        venue_filter=venue_filter,
    )
    for pub in results:
        t = pub.get("title", "")
        if t not in seen_titles:
            candidates.append(pub)
            seen_titles.add(t)

    results = search(
        title,
        max_results=max_results * 2,
        year_from=year_from,
        year_to=year_to,
        venue_filter=venue_filter,
    )
    for pub in results:
        t = pub.get("title", "")
        if t not in seen_titles:
            candidates.append(pub)
            seen_titles.add(t)

    filtered = []
    for pub in candidates:
        pub_title = pub.get("title", "")
        ratio = difflib.SequenceMatcher(None, title.lower(), pub_title.lower()).ratio()
        if ratio >= similarity_threshold:
            pub["similarity"] = ratio
            filtered.append(pub)

    filtered = sorted(filtered, key=lambda x: x.get("similarity", 0), reverse=True)
    filtered = filtered[:max_results]

    if include_bibtex:
        for pub in filtered:
            if pub.get("dblp_key"):
                bibtex = fetch_bibtex_entry(pub["dblp_key"])
                if bibtex:
                    pub["bibtex"] = bibtex

    return filtered


def fetch_and_process_bibtex(url: str, new_key: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        bibtex = response.text
        bibtex = re.sub(r"@(\w+){([^,]+),", r"@\1{" + new_key + ",", bibtex, count=1)
        return bibtex
    except requests.exceptions.Timeout:
        return f"% Error: Timeout fetching {url} after {REQUEST_TIMEOUT} seconds"
    except Exception as e:
        return f"% Error fetching {url}: {e}"


def fetch_bibtex_entry(dblp_key: str) -> str:
    try:
        if not dblp_key or dblp_key.isspace():
            return ""

        urls_to_try = [f"https://dblp.org/rec/{dblp_key}.bib"]
        if ":" in dblp_key:
            urls_to_try.append(f"https://dblp.org/rec/{dblp_key.replace(':', '/')}.bib")

        for url in urls_to_try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200 and response.text.strip():
                bibtex = response.text
                citation_key_match = re.match(r"@(\w+){([^,]+),", bibtex)
                if citation_key_match:
                    old_key = citation_key_match.group(2)
                    author_year_match = re.search(r"([A-Z][a-z]+).*?(\\d{2,4})", dblp_key)
                    if author_year_match:
                        author = author_year_match.group(1)
                        year = author_year_match.group(2)
                        if len(year) == 2:
                            year = "20" + year if int(year) < 50 else "19" + year
                        new_key = f"{author}{year}"
                    else:
                        parts = dblp_key.split("/")
                        new_key = parts[-1] if parts else dblp_key
                    bibtex = bibtex.replace(f"{{{old_key},", f"{{{new_key},", 1)
                return bibtex
        return ""
    except requests.exceptions.Timeout:
        return f"% Error: Timeout fetching BibTeX for {dblp_key} after {REQUEST_TIMEOUT} seconds"
    except Exception as e:
        return f"% Error: An unexpected error occurred while fetching BibTeX for {dblp_key}: {e}"


def get_venue_info(venue_name: str) -> Dict[str, Any]:
    try:
        url = "https://dblp.org/search/venue/api"
        params = {"q": venue_name, "format": "json", "h": 1}
        response = requests.get(url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        hits = data.get("result", {}).get("hits", {})
        total = int(hits.get("@total", "0"))

        if total > 0:
            hit = hits.get("hit", [])
            if isinstance(hit, list):
                hit = hit[0]

            info = hit.get("info", {})
            return {
                "venue": info.get("venue", ""),
                "acronym": info.get("acronym", ""),
                "type": info.get("type", ""),
                "url": info.get("url", ""),
            }
        return {"venue": "", "acronym": "", "type": "", "url": ""}
    except Exception:
        return {"venue": "", "acronym": "", "type": "", "url": ""}


def calculate_statistics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    authors = Counter()
    venues = Counter()
    years = []

    for result in results:
        for author in result.get("authors", []):
            authors[author] += 1

        venue = result.get("venue", "")
        if isinstance(venue, list):
            venue = ", ".join(venue) if venue else ""
        venues[venue or "(empty)"] += 1

        year = result.get("year")
        if year:
            with contextlib.suppress(ValueError, TypeError):
                years.append(int(year))

    return {
        "total_publications": len(results),
        "time_range": {"min": min(years) if years else None, "max": max(years) if years else None},
        "top_authors": sorted(authors.items(), key=lambda x: x[1], reverse=True),
        "top_venues": sorted(venues.items(), key=lambda x: x[1], reverse=True),
    }


def cmd_search(args: argparse.Namespace) -> None:
    result = search(
        query=args.query,
        max_results=args.max_results,
        year_from=args.year_from,
        year_to=args.year_to,
        venue_filter=args.venue_filter,
        include_bibtex=args.include_bibtex,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_fuzzy(args: argparse.Namespace) -> None:
    result = fuzzy_title_search(
        title=args.title,
        similarity_threshold=args.similarity_threshold,
        max_results=args.max_results,
        year_from=args.year_from,
        year_to=args.year_to,
        venue_filter=args.venue_filter,
        include_bibtex=args.include_bibtex,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_author(args: argparse.Namespace) -> None:
    result = get_author_publications(
        author_name=args.name,
        similarity_threshold=args.similarity_threshold,
        max_results=args.max_results,
        include_bibtex=args.include_bibtex,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_venue(args: argparse.Namespace) -> None:
    result = get_venue_info(args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats(args: argparse.Namespace) -> None:
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit("statistics input must be a JSON array of publication objects")
    result = calculate_statistics(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_add_bibtex(args: argparse.Namespace) -> None:
    dblp_key = args.dblp_key.strip()
    if dblp_key.endswith(".bib"):
        dblp_key = dblp_key[:-4]
    if "dblp.org/rec/" in dblp_key:
        dblp_key = dblp_key.split("dblp.org/rec/")[-1]

    url = f"https://dblp.org/rec/{dblp_key}.bib"
    bibtex = fetch_and_process_bibtex(url, args.citation_key)
    if bibtex.strip().startswith("% Error"):
        raise SystemExit(f"Failed to add entry: {bibtex}")

    state = _load_state()
    state.setdefault("entries", {})[args.citation_key] = bibtex
    _save_state(state)
    count = len(state["entries"])
    print(
        json.dumps(
            {
                "message": f"Added {args.citation_key}",
                "count": count,
                "state_path": STATE_PATH,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_export(args: argparse.Namespace) -> None:
    state = _load_state()
    entries = list(state.get("entries", {}).values())
    if not entries:
        raise SystemExit("Collection is empty. Add entries using add-bibtex first.")

    path = args.path
    if not path.endswith(".bib"):
        path = f"{path}.bib"

    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry)
            f.write("\n\n")

    state["entries"] = {}
    _save_state(state)

    print(
        json.dumps(
            {"message": f"Exported {len(entries)} references", "path": path},
            ensure_ascii=False,
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DBLP CLI (Codex skill wrapper)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Boolean search")
    p_search.add_argument("--query", required=True)
    p_search.add_argument("--max-results", type=int, default=10)
    p_search.add_argument("--year-from", type=int)
    p_search.add_argument("--year-to", type=int)
    p_search.add_argument("--venue-filter")
    p_search.add_argument("--include-bibtex", action="store_true")
    p_search.set_defaults(func=cmd_search)

    p_fuzzy = sub.add_parser("fuzzy", help="Fuzzy title search")
    p_fuzzy.add_argument("--title", required=True)
    p_fuzzy.add_argument("--similarity-threshold", type=float, required=True)
    p_fuzzy.add_argument("--max-results", type=int, default=10)
    p_fuzzy.add_argument("--year-from", type=int)
    p_fuzzy.add_argument("--year-to", type=int)
    p_fuzzy.add_argument("--venue-filter")
    p_fuzzy.add_argument("--include-bibtex", action="store_true")
    p_fuzzy.set_defaults(func=cmd_fuzzy)

    p_author = sub.add_parser("author", help="Author search with fuzzy matching")
    p_author.add_argument("--name", required=True)
    p_author.add_argument("--similarity-threshold", type=float, required=True)
    p_author.add_argument("--max-results", type=int, default=20)
    p_author.add_argument("--include-bibtex", action="store_true")
    p_author.set_defaults(func=cmd_author)

    p_venue = sub.add_parser("venue", help="Venue lookup")
    p_venue.add_argument("--name", required=True)
    p_venue.set_defaults(func=cmd_venue)

    p_stats = sub.add_parser("stats", help="Calculate statistics from JSON results")
    p_stats.add_argument(
        "--input",
        required=True,
        help="Path to JSON array of publications or '-' for stdin",
    )
    p_stats.set_defaults(func=cmd_stats)

    p_add = sub.add_parser("add-bibtex", help="Add BibTeX entry to collection")
    p_add.add_argument("--dblp-key", required=True)
    p_add.add_argument("--citation-key", required=True)
    p_add.set_defaults(func=cmd_add_bibtex)

    p_export = sub.add_parser("export-bibtex", help="Export collected BibTeX entries")
    p_export.add_argument("--path", required=True)
    p_export.set_defaults(func=cmd_export)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.ERROR)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
