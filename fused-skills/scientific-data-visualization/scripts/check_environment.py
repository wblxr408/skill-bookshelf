#!/usr/bin/env python3
"""Verify the runtime dependencies required by the public skill scripts.

This check is intentionally offline: it neither installs nor upgrades packages.
It makes a fresh-environment failure explicit before data are read or artifacts
are written.
"""
from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "scripts" / "requirements.txt"
MODULES = {
    "pandas": "pandas", "numpy": "numpy", "matplotlib": "matplotlib",
    "PyYAML": "yaml", "openpyxl": "openpyxl", "scipy": "scipy",
    "statsmodels": "statsmodels", "scikit-learn": "sklearn",
    "Pillow": "PIL", "joblib": "joblib",
}


def version_key(value: str) -> tuple[int, ...]:
    """Compare release components without importing a non-declared helper."""
    return tuple(int(item) for item in re.findall(r"\d+", value)[:4])


def requirement_lines(path: Path) -> list[tuple[str, str | None]]:
    parsed = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)(?:>=([A-Za-z0-9_.-]+))?", line)
        if not match:
            raise ValueError(f"Unsupported requirement format: {line}")
        parsed.append((match.group(1), match.group(2)))
    return parsed


def check() -> dict[str, Any]:
    requirements = requirement_lines(REQUIREMENTS)
    packages: list[dict[str, Any]] = []
    for distribution, minimum in requirements:
        module = MODULES.get(distribution)
        present = bool(module and importlib.util.find_spec(module))
        installed = None
        try:
            installed = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            present = False
        compatible = present and (minimum is None or version_key(installed or "0") >= version_key(minimum))
        packages.append({"distribution": distribution, "module": module, "minimum": minimum, "installed": installed, "status": "passed" if compatible else "failed"})
    return {
        "status": "passed" if all(item["status"] == "passed" for item in packages) else "failed",
        "python": sys.version.split()[0], "requirements": str(REQUIREMENTS.resolve()), "packages": packages,
    }


def main() -> None:
    report = check()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "passed" else 2)


if __name__ == "__main__":
    main()
