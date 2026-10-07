#!/usr/bin/env python3
"""Fail on unresolved references, fatal diagnostics, or missing PDF output."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

PATTERNS = (
    r"^!", r"Emergency stop", r"Fatal error",
    r"Missing character:", r"There were undefined (?:references|citations)",
    r"(?:Reference|Citation) [^\n]*(?:\n[^\n]*)?\bundefined\b",
    r"multiply[ -]defined", r"Label [^\n]* multiply defined",
    r"Rerun to get cross-references right", r"Rerun to get /PageLabels entry",
    r"Package rerunfilecheck Warning:",
)


def problems(text: str) -> list[str]:
    """Return actionable failures from a final (not intermediate-pass) log."""
    found = []
    for pattern in PATTERNS:
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if match:
            found.append(match.group(0).strip())
    if not re.search(r"Output written on .+\.pdf", text):
        found.append("No successful PDF-output record in the log")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    args = parser.parse_args()
    try:
        failures = problems(args.log.read_text(encoding="utf-8", errors="replace"))
    except OSError as exc:
        print(f"Cannot read LaTeX log: {exc}", file=sys.stderr)
        return 1
    if failures:
        print("LaTeX validation failed:\n" + "\n".join(failures), file=sys.stderr)
        return 1
    print("Final LaTeX log: PDF produced; citations, references and glyphs resolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
