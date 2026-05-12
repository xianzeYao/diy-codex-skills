#!/usr/bin/env python3
"""Render/crop PDF figures into local PNG assets for Notion UI paste.

This script prepares local PNGs; Notion cannot embed local filesystem paths
directly through the connector. Paste/upload the generated PNGs through the
Notion UI with Computer Use so Notion stores them as internal files.

Examples:
    prepare_notion_figures.py paper.pdf --out-dir assets/tracevla --pages 1 3 8
    prepare_notion_figures.py paper.pdf --out-dir assets/tracevla --pages 3 \
      --crop 3:0,80,612,420
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image


def parse_crop(value: str) -> tuple[int, tuple[int, int, int, int]]:
    page, box = value.split(":", 1)
    left, top, right, bottom = [int(part) for part in box.split(",")]
    if right <= left or bottom <= top:
        raise argparse.ArgumentTypeError(f"invalid crop box: {value}")
    return int(page), (left, top, right, bottom)


def render_with_pymupdf(pdf: Path, out_dir: Path, pages: Iterable[int], dpi: int) -> dict[int, Path] | None:
    try:
        import fitz  # type: ignore
    except Exception:
        return None

    doc = fitz.open(str(pdf))
    rendered: dict[int, Path] = {}
    scale = dpi / 72
    matrix = fitz.Matrix(scale, scale)
    for page_num in pages:
        page = doc[page_num - 1]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out = out_dir / f"page-{page_num:03d}.png"
        pix.save(str(out))
        rendered[page_num] = out
    return rendered


def render_with_pdf2image(pdf: Path, out_dir: Path, pages: Iterable[int], dpi: int) -> dict[int, Path] | None:
    if not shutil.which("pdftoppm"):
        return None
    try:
        from pdf2image import convert_from_path
    except Exception:
        return None

    rendered: dict[int, Path] = {}
    for page_num in pages:
        images = convert_from_path(str(pdf), dpi=dpi, first_page=page_num, last_page=page_num)
        out = out_dir / f"page-{page_num:03d}.png"
        images[0].save(out)
        rendered[page_num] = out
    return rendered


def render_with_sips(pdf: Path, out_dir: Path, pages: Iterable[int]) -> dict[int, Path] | None:
    """Fallback for macOS. `sips` usually renders only the first PDF page."""
    if not shutil.which("sips"):
        return None
    requested = list(pages)
    if requested != [1]:
        return None
    out = out_dir / "page-001.png"
    subprocess.run(
        ["sips", "-s", "format", "png", str(pdf), "--out", str(out)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return {1: out}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--pages", type=int, nargs="+", required=True, help="1-based page numbers")
    parser.add_argument("--crop", type=parse_crop, action="append", default=[], help="page:left,top,right,bottom")
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    pages = sorted(set(args.pages))

    rendered = (
        render_with_pymupdf(args.pdf, args.out_dir, pages, args.dpi)
        or render_with_pdf2image(args.pdf, args.out_dir, pages, args.dpi)
        or render_with_sips(args.pdf, args.out_dir, pages)
    )
    if rendered is None:
        print(
            "No PDF rendering backend available. Install PyMuPDF or poppler, "
            "or render screenshots manually before pasting them into Notion.",
            file=sys.stderr,
        )
        return 1

    assets: list[dict[str, str | int]] = []
    for page_num, path in rendered.items():
        assets.append({"page": page_num, "file": str(path)})

    for page_num, box in args.crop:
        if page_num not in rendered:
            print(f"crop references page {page_num}, but it was not rendered", file=sys.stderr)
            return 2
        image = Image.open(rendered[page_num])
        cropped = image.crop(box)
        out = args.out_dir / f"page-{page_num:03d}-crop-{len(assets)+1:02d}.png"
        cropped.save(out)
        assets.append({"page": page_num, "file": str(out), "crop": ",".join(map(str, box))})

    manifest = args.out_dir / "manifest.json"
    manifest.write_text(json.dumps({"assets": assets}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
