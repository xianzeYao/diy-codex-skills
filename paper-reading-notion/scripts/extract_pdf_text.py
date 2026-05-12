#!/usr/bin/env python3
"""Extract page-delimited text from a PDF.

Usage:
    extract_pdf_text.py input.pdf output.txt
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: extract_pdf_text.py input.pdf output.txt", file=sys.stderr)
        return 2

    pdf_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    reader = PdfReader(str(pdf_path))

    chunks: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"\n\n--- PAGE {index} ---\n{text}")

    out_path.write_text("".join(chunks), encoding="utf-8")
    print(f"pages={len(reader.pages)} chars={sum(len(c) for c in chunks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
