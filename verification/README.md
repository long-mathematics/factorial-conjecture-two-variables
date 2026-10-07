# Verification records

`make test` regenerates `degree6.json`, `identities.json`, and `supplementary.json`. These reports are ignored by Git and uploaded by CI. They record finite exact checks, not a proof or formal verification of FC(2), analytic continuation, or EIT I. The supplementary report identifies the precise manuscript SHA-256 tested.

`pdf_snapshot.json` is tracked. `make snapshot` rebuilds the manuscript and records fingerprints of the LaTeX source, Makefile, snapshot script, and browser-facing PDF, together with the compiler version. Commit the manifest and root PDF together. `make snapshot-check` validates those fingerprints without assuming that builds on different systems produce identical PDF bytes.

The snapshot checks certify consistency of recorded files, not mathematical correctness. Release-tool regression tests include deliberately stale sources, changed PDFs, malformed manifests, missing glyphs, and undefined references/citations.
