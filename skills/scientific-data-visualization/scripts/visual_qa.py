#!/usr/bin/env python3
"""Deterministic image-level checks for rendered scientific figures.

This is a machine gate, not a replacement for human/AI visual review. It checks
that exported images are non-empty, have the requested raster resolution, retain
usable tonal variation, and can be inspected in grayscale.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageStat


def audit_image(path: Path, min_dpi: int = 300) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    with Image.open(path) as image:
        array = np.asarray(image.convert("RGB"), dtype=np.uint8)
        info = image.info
        dpi = info.get("dpi")
        dpi_x = float(dpi[0]) if isinstance(dpi, tuple) else None
        # PNG metadata stores the requested integer DPI as a rounded pixels-per-
        # metre value (e.g. 299.9994 for 300); allow that representation error.
        if path.suffix.lower() == ".png" and dpi_x is not None and dpi_x + 0.5 < min_dpi:
            errors.append(f"PNG DPI {dpi_x:.1f} is below required {min_dpi}.")
        if array.size == 0 or float(array.std()) < 1.0:
            errors.append("Rendered image is blank or has no usable tonal variation.")
        gray = np.dot(array[..., :3], [0.2126, 0.7152, 0.0722])
        if float(gray.std()) < 3.0:
            warnings.append("Grayscale contrast is very low; inspect labels and category distinguishability manually.")
        unique_gray = int(np.unique(np.round(gray).astype(np.uint8)).size)
        return {"path": str(path), "width_px": int(image.width), "height_px": int(image.height), "dpi": dpi_x, "grayscale_levels": unique_gray, "errors": errors, "warnings": warnings, "status": "failed" if errors else "passed"}


def audit_paths(paths: list[Path], min_dpi: int = 300) -> dict[str, Any]:
    results = []
    for path in paths:
        if not path.exists():
            results.append({"path": str(path), "status": "failed", "errors": ["Output file does not exist."], "warnings": []})
        elif path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            results.append(audit_image(path, min_dpi=min_dpi))
        else:
            results.append({"path": str(path), "status": "skipped", "errors": [], "warnings": ["Raster image-level checks do not inspect vector geometry; open the SVG/PDF for human review."]})
    return {"status": "failed" if any(item["status"] == "failed" for item in results) else "passed", "human_review_required": True, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--min-dpi", type=int, default=300)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit_paths(args.images, args.min_dpi)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
    raise SystemExit(0 if report["status"] == "passed" else 2)


if __name__ == "__main__":
    main()
