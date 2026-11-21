# Hexagon reference update — 21 November 2026

This update starts from `8b1eb46ff530122ed25f588b78bf9fdc98cb9577` and prepares the manuscript for submission to Hexagon.

The EIT I bibliography entry now cites the published, version-specific record [hexagon:2611.00736v1](https://hexagonmath.org/2611.00736v1) and its source. Hexagon's public source SHA-256 agrees exactly with the reviewed source at repository commit `92db79eedeb064694ff20e9201d73fc2bc0857f4`. The stated nonvanishing input remains Corollary 1.4, source label `cor:single`; it applies to a nonconstant algebraic polynomial, distinct algebraic endpoints, and a nonzero algebraic parameter. The previous source pin remains in the reference ledger for provenance.

EIT II and III are also published, as `2611.00737v1` and `2611.00738v1`. They are recorded in the README for context but are not direct dependencies and have not been added to this manuscript's bibliography. Publication on Hexagon is not represented as independent peer review. This update does not re-audit the EIT proof or change any mathematical claim.

The reproducibility paragraph now points to the accompanying repository, which hosts the exact-check scripts; the manuscript-only Hexagon source package need not contain those scripts. The manuscript revision date, citation metadata, tracked PDF, and snapshot fingerprints are refreshed together.

Validation: the existing 17 exact degree-six checks, 405 identity checks, eight supplementary groups (including 70,215 radial coefficient tuples), and 11 release-tool tests passed. The updated manuscript builds with shell escape disabled, its final log has no unresolved citations/references, duplicate labels, or missing glyphs, and all 12 bibliography entries are cited. The tracked PDF and source fingerprints agree, and all 20 rendered pages were visually inspected. These are preparation and reproducibility checks, not formal verification of FC(2).
