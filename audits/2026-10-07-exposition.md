# Expository and reference revision — 7 October 2026

## Scope

This revision starts from `49f36a4c0e3d691c5d4a2c432308987ef07d62fc`. It implements the preceding model-assisted proof-read recommendations without changing the nonflat proof architecture or removing the separate EIT I input to the general flat case. Theorem/lemma/proposition numbering and all original source labels are retained. Appendix B remains in the manuscript, explicitly auxiliary, to avoid unnecessary restructuring.

The source and PDF for a released snapshot are identified by `verification/pdf_snapshot.json`. This note records work performed, not external refereeing, formal verification, or a new audit of the EIT proof.

## Mathematical exposition

The revision makes the flat/nonflat distinction explicit in the abstract, introduction, and README; corrects the specialization degree justification; gives a direct Mittag–Leffler growth bound; and expands compact-set uniformity, the entire logarithmic coefficient's contour formula (with its prefactor), and the continued remainder estimates.

The leaf argument now specifies the sphere complement, chosen slit/root/logarithm, and fractional-class monodromy separation. Retained histories remain away from the zero-top locus, and only their negative Puiseux coefficients factor through permutations. Geometric infinity labeling, orbitwise averaging, separating chords, rational complexification, and endpoint leaf-germ evaluation are stated explicitly.

The radial-limit bound uses distinct notation for coefficient suprema. An unnumbered remark identifies the elementary affine-exponent flat subcase, with its coefficient constraints retained during specialization. No numerical convergence rate is promoted to a theorem.

## Sources checked

- Pakovich–Muzychuk, arXiv:0710.4085v2: Theorem 3.1 and Section 4.1/Proposition 4.1 were checked against PDF page images (printed pages 13 and 21). Version-specific pointers also identify Sections 2.1–2.2 and Propositions 2.4 and 2.6. Journal-typeset numbering is not asserted.
- EIT I at `22d98c4f27e606b5b25fa673c33f9c56c53cc86b`: the quoted single-integral statement, source label `cor:single` (Corollary 1.4), and author metadata were checked in the pinned LaTeX. Its proof is an assumed external input in this revision, not independently re-audited here.
- Moura, arXiv:math/0312323, Section 2, Theorem 1: the analytic total-pole-order formulation was checked on printed page 3. Appendix B supplies the polynomial-presentation/formal version and explains the degree-bound conversion, including when the denominator degree is strictly below its bound.
- The pinned `openai/math` multiplicity prose and Lean declaration were inspected for their hypotheses and attribution. The prose assumes exact denominator degree; the Lean declaration uses an upper bound. Bostan–Dumas is now cited as the primary source for the formal-series Wronskian argument. Reading the Lean declaration is not a claim that this manuscript has been formalized or that the imported project was rebuilt here.

## Checks and limits

The original scripts were preserved and run: 17 exact degree-six checks and 405 symbolic checks passed. The cleaned supplementary script asserts every result and passes eight groups, including all 70,215 admissible `(D,n,K,J)` tuples with `1 <= D <= 6` and `0 <= n < 30`, the quadratic sheet coefficient through order five, the moving-root differential for `D=2,...,8`, and the displayed connection, determinant, and collision values/weights.

Eleven release-tool tests exercise clean and failing LaTeX logs and current/stale/modified snapshot fixtures. The revised manuscript was compiled, its final citations and references resolved, and its rendered pages inspected. Generated reports are reproduced by `make test` and retained as CI artifacts; they are not universal proof certificates.

The unspecified complex-cubic numerical experiment reported in the conversation is not recorded as reproduced. Likewise, the supplementary tuple grid is not described as a test of every possible polynomial. No error estimate stronger than the manuscript's uniform `o(1)` is inferred from it.

## Release workflow

The root PDF and fingerprint manifest are refreshed together. CI validates their consistency and retains exact-check reports and the final log. Routine CI remains read-only; refreshing a snapshot is an explicit release operation. Local builds can differ in PDF metadata from CI builds, so validation compares the committed PDF with its own recorded fingerprint rather than with a new build's bytes.


## Follow-up: product-exponential Integral/Mathieu consequence

A short corollary was added after FC(2). For the product-exponential measure
$e^{-x-y}\,dx\,dy$ on $(0,\infty)^2$, its zero-integral polynomial space is
exactly $\ker\mathcal L$. The proof records the stronger tail statement:
if $\mathcal L(f^m)=0$ for every sufficiently large $m$, then applying FC(2)
to $f^N$ for a suitable $N$ gives $f=0$. The Mathieu--Zhao conclusion is then
immediate.

The historical framing was checked against Arno van den Essen,
*The Amazing Image Conjecture*, arXiv:1006.5801v1, which states the Integral
Conjecture, and against van den Essen--Wright--Zhao, *On the Image
Conjecture*, which introduced the Factorial Conjecture in the same program.
Accordingly, the manuscript does not claim that the FC--Mathieu connection
is new; it claims only the consequence of the present FC(2) theorem for this
specific two-dimensional measure. No claim of an exhaustive literature
search for independent proofs is made here.
