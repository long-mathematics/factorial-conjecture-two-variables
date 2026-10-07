#!/usr/bin/env python3
"""Refresh or validate the tracked PDF and its source-fingerprint manifest.

Validation compares the committed PDF with its recorded hash, not with a new
PDF's bytes: compiler versions and metadata can legitimately change those bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

INPUTS = (
    "paper/factorial_conjecture_two_variables.tex",
    "Makefile",
    "scripts/check_pdf_snapshot.py",
)
PDF = "factorial_conjecture_two_variables.pdf"
BUILT_PDF = "output/pdf/" + PDF
MANIFEST = "verification/pdf_snapshot.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root: Path) -> list[str]:
    try:
        manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
            return ["Unsupported snapshot-manifest format"]
        sources = manifest.get("inputs_sha256")
        if not isinstance(sources, dict) or set(sources) != set(INPUTS):
            return ["Snapshot input list is missing or unexpected"]
        failures = [f"Stale snapshot input: {path}" for path in INPUTS
                    if digest(root / path) != sources[path]]
        pdf = root / PDF
        if not pdf.read_bytes().startswith(b"%PDF-"):
            failures.append("Tracked snapshot is not a PDF")
        if manifest.get("pdf_path") != PDF or digest(pdf) != manifest.get("pdf_sha256"):
            failures.append("Tracked PDF does not match its recorded fingerprint")
        return failures
    except (OSError, ValueError, TypeError) as exc:
        return [f"Cannot validate snapshot: {exc}"]


def write(root: Path) -> None:
    built = root / BUILT_PDF
    if not built.read_bytes().startswith(b"%PDF-"):
        raise ValueError(f"Not a PDF: {built}")
    shutil.copyfile(built, root / PDF)
    compiler = subprocess.run(["pdflatex", "--version"], check=True,
                              capture_output=True, text=True).stdout.splitlines()[0]
    data = {
        "schema_version": 1,
        "inputs_sha256": {path: digest(root / path) for path in INPUTS},
        "pdf_path": PDF,
        "pdf_sha256": digest(root / PDF),
        "compiler": compiler,
        "refresh_command": "make snapshot",
        "scope": "Source/PDF consistency only; not mathematical verification.",
    }
    target = root / MANIFEST
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        if args.write:
            write(args.root)
        failures = validate(args.root)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        failures = [str(exc)]
    if failures:
        print("Snapshot validation failed:\n" + "\n".join(failures)
              + "\nRun make snapshot and commit the PDF and manifest together.", file=sys.stderr)
        return 1
    print("Tracked PDF and source fingerprints agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
