#!/usr/bin/env python3
"""Regression tests for release checks, including deliberately stale artifacts."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import check_latex_log as logcheck
import check_pdf_snapshot as snapshot


class LogTests(unittest.TestCase):
    clean = "This is pdfTeX\nOutput written on output/paper.pdf (20 pages).\n"

    def test_clean(self):
        self.assertEqual(logcheck.problems(self.clean), [])

    def test_undefined_reference(self):
        text = self.clean + "LaTeX Warning: Reference `x' on page 1 undefined on input line 5.\n"
        self.assertTrue(logcheck.problems(text))

    def test_undefined_citation_wrapped(self):
        text = self.clean + "LaTeX Warning: Citation `long-citation' on page 10\nundefined on input line 123.\n"
        self.assertTrue(logcheck.problems(text))

    def test_missing_glyph(self):
        self.assertTrue(logcheck.problems(self.clean + "Missing character: There is no X!\n"))

    def test_no_output(self):
        self.assertTrue(logcheck.problems("No compiler output here."))

    def test_duplicate_label(self):
        self.assertTrue(logcheck.problems(self.clean + "LaTeX Warning: Label `a' multiply defined.\n"))


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in snapshot.INPUTS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("test input: " + name, encoding="utf-8")
        (self.root / snapshot.PDF).write_bytes(b"%PDF-1.4\ntest fixture\n")
        data = {"schema_version": 1, "pdf_path": snapshot.PDF,
                "inputs_sha256": {p: snapshot.digest(self.root / p) for p in snapshot.INPUTS},
                "pdf_sha256": snapshot.digest(self.root / snapshot.PDF)}
        manifest = self.root / snapshot.MANIFEST
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(data), encoding="utf-8")

    def test_current_snapshot(self):
        self.assertEqual(snapshot.validate(self.root), [])

    def test_stale_source(self):
        (self.root / snapshot.INPUTS[0]).write_text("changed", encoding="utf-8")
        self.assertTrue(snapshot.validate(self.root))

    def test_modified_pdf(self):
        (self.root / snapshot.PDF).write_bytes(b"%PDF-1.4\ndifferent fixture\n")
        self.assertTrue(snapshot.validate(self.root))

    def test_missing_manifest(self):
        (self.root / snapshot.MANIFEST).unlink()
        self.assertTrue(snapshot.validate(self.root))

    def test_invalid_manifest(self):
        (self.root / snapshot.MANIFEST).write_text("[]", encoding="utf-8")
        self.assertTrue(snapshot.validate(self.root))


if __name__ == "__main__":
    unittest.main()
