# Factorial Conjecture in Two Variables

This repository contains an unpublished research manuscript proving the two-variable Factorial Conjecture

$
\mathcal{L}(x^a y^b)=a!b!,\qquad
\left(\mathcal{L}(f^n)=0\text{ for all }n\ge 1\right)\Longrightarrow f=0.
$

The nonflat case is proved using an exact radial Mittag--Leffler transform, full leaf transport with retained continuation histories, polynomial monodromy/path modules, trace orthogonality, and Lindemann--Weierstrass. The constant projective-leading case uses the explicitly stated single-integral nonvanishing theorem from EIT I.

## Status

The manuscript is **unpublished and unrefereed**. Supporting symbolic checks verify finite identities used in examples and auxiliary calculations; they are not a formal verification of FC(2), analytic continuation, polynomial monodromy, or the EIT I input.

## Repository layout

- `paper/factorial_conjecture_two_variables.tex` — standalone LaTeX manuscript.
- `scripts/verify_degree6.py` — exact rational-arithmetic checks for the degree-six collision example.
- `scripts/verify_identities.py` — symbolic checks for kernel and auxiliary identities.
- `verification/` — generated exact-check records.
- `.github/workflows/latex.yml` — CI build and verification workflow.
- `CITATION.cff` — citation metadata.
- `LICENSE.md` — dual-license notice.

## Build

With TeX Live and `latexmk`:

```sh
make
```

This builds:

```text
output/pdf/factorial_conjecture_two_variables.pdf
```

Run the exact checks with:

```sh
make test
```

The current suite contains 17 degree-six checks and 405 symbolic checks.

## Mathematical dependencies

The nonflat argument uses classical Lindemann--Weierstrass and the rational top-component irreducibility theorem of Pakovich--Muzychuk. The endpoint averaging, planar separation, actual path-module containment, analytic leaf transport, block traces, and arithmetic pairing used in the proof are developed in the manuscript.

The flat conclusion uses the single-integral nonvanishing corollary of EIT I.

The October 2026 `openai/math` release influenced proof exploration and supplied useful comparison tools, but no theorem from that release is a dependency of the main FC(2) proof. Appendix B discusses Claire Moura's multiplicity estimate and the formal treatment of that estimate in `openai/math` as a potentially useful finite-certificate tool.

## License

The manuscript and mathematical exposition are licensed under **CC BY 4.0**. Code and build tooling are licensed under the **MIT License**. See `LICENSE.md`.
