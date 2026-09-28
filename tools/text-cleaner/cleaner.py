#!/usr/bin/env python3
"""
Simple Text Cleaner
Cleans messy text from PDFs, WhatsApp chats, or copied content.

Usage:
    python cleaner.py input.txt
    python cleaner.py input.txt --output clean.txt
"""

import argparse
import re
import sys
from pathlib import Path


def clean_text(text: str) -> str:
    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize newlines (max 2 consecutive)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace on each line
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)

    # Remove common PDF artifacts
    text = re.sub(r"\x0c", "", text)  # form feed
    text = text.replace("\xa0", " ")  # non-breaking space

    # Fix common broken words from PDF copy (simple heuristic)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    return text.strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Clean messy text files")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("--output", "-o", help="Output file (default: print to stdout)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found → {input_path}", file=sys.stderr)
        sys.exit(1)

    raw = input_path.read_text(encoding="utf-8", errors="ignore")
    cleaned = clean_text(raw)

    if args.output:
        Path(args.output).write_text(cleaned, encoding="utf-8")
        print(f"Cleaned text saved to → {args.output}")
    else:
        print(cleaned)


if __name__ == "__main__":
    main()
