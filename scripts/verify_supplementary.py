#!/usr/bin/env python3
"""Supplementary exact checks; not a proof of FC(2), continuation, or EIT I.

Adapted from the reproducible checks accompanying the 7 October 2026 audit.
Every reported group must pass. No network, numerical quadrature, or OCR is used.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import platform

import sympy as s


def main() -> None:
    passed: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        passed.append(name)

    t, w = s.symbols("t w")
    A, B, D = t**2 + 1, t, 2
    modulus = s.Poly(A - w, t, domain=s.QQ.frac_field(w))
    inverse = s.invert(s.Poly(s.diff(A, t), t, domain=s.QQ.frac_field(w)), modulus).as_expr()
    rows = []
    for j in range(2):
        raw = ((j*t**(j-1)*inverse if j else 0) - t**j*s.diff(A, t, 2)*inverse**2
               + t**j*s.diff(B, t)*inverse/(D*w) - t**j*B/(D*w**2))
        reduced = s.Poly(raw, t, domain=s.QQ.frac_field(w)).rem(modulus)
        rows.append([s.factor(reduced.nth(k)) for k in range(2)])
    expected = s.Matrix([[-1/(2*(w-1)), (2-w)/(4*w**2*(w-1))], [(2-w)/(4*w**2), 0]])
    check("rational connection (Appendix B.2)", all(s.cancel(entry) == 0 for entry in s.Matrix(rows)-expected))

    a, b, c = s.symbols("a b c")
    q = (w-a)*(w-b)
    matrix = s.Matrix([[0, -1/q, 0], [0, -c/w**2, 0], [0, 0, 0]])
    observation = [s.Matrix([[1, 0, -1/w]])]
    for _ in range(2):
        observation.append(observation[-1].diff(w) + observation[-1]*matrix)
    determinant = s.Matrix.vstack(*observation).det()
    target = (-(a+b+c)*w**2 + (2*a*b+c*(a+b))*w - c*a*b)/(q**2*w**4)
    check("observation determinant (Appendix B.3)", s.factor(determinant-target) == 0)

    top = s.chebyshevt(6, 2*t-1)-1
    points = [(2-s.sqrt(3))/4, s.Rational(1, 2), (2+s.sqrt(3))/4]
    quadratic = [s.simplify(s.diff(top, t, 2).subs(t, point)/2) for point in points]
    check("collision values (Appendix C)", all(s.simplify(top.subs(t, point)+2) == 0
                                              for point in points))
    check("collision quadratic coefficients (Appendix C)", quadratic == [288, 72, 288])
    weights = [1/(2*coefficient) for coefficient in quadratic]
    check("collision positive weights (Appendix C)",
          weights == [s.Rational(1, 576), s.Rational(1, 144), s.Rational(1, 576)])

    count = 0
    for degree in range(1, 7):
        for n in range(30):
            factorials = [math.factorial(i) for i in range(degree*n+2)]
            for K in range(n+1):
                falling = math.factorial(n)//math.factorial(n-K)
                for J in range(K, degree*K+1):
                    if not 0 < falling*factorials[degree*n-J+1] <= factorials[degree*n+1]:
                        raise AssertionError(f"radial bound: D={degree}, n={n}, K={K}, J={J}")
                    count += 1
    check("radial coefficient grid (Lemma 6.1)", count == 70215)

    rho, u = s.symbols("rho u")
    delta = sum(-s.binomial(s.Rational(1, 2), j)*(-c)**j*u**(2*j-1) for j in range(1, 6))
    series = s.series(s.exp(delta), c, 0, 6).removeO().expand()
    reverted = sum(rho*s.Rational(1, 2)*(-1)**m*series.coeff(u, m)
                   *(1-rho)**(m-1)/s.factorial(m-1) for m in range(1, 10))
    beta = -c*rho/4*sum((c*(rho**2-1)/4)**j/(s.factorial(j)*s.factorial(j+1))
                       for j in range(5))
    check("quadratic sheet coefficient through c^5 (Appendix A.2)", s.expand(reverted-beta) == 0)

    L, root = s.symbols("L root", nonzero=True)
    check("moving lower-root differential, D=2..8 (Appendix A.3)", all(
        s.simplify((L/root)**(degree-1)/(degree*L**degree)*(c/L)*s.exp(c/L)
                   + s.diff(s.exp(c/L), L)/(degree*root**(degree-1))) == 0
        for degree in range(2, 9)))

    base = Path(__file__).resolve().parents[1]
    source = base / "paper/factorial_conjecture_two_variables.tex"
    result = {
        "purpose": "Finite exact regression checks only; not mathematical or formal verification of FC(2).",
        "python": platform.python_version(), "sympy": s.__version__,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "check_groups": len(passed), "radial_tuples_checked": count, "passed_groups": passed,
    }
    output = base / "verification/supplementary.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{len(passed)} supplementary groups passed, including {count} radial tuples; wrote {output}")


if __name__ == "__main__":
    main()
