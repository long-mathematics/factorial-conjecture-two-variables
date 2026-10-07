#!/usr/bin/env python3
"""Exact finite checks for factorial_conjecture_two_variables.tex; not a verification of the general proof.

Requires Python 3 and SymPy. Writes verification/identities.json in the repository root.
No network access or numerical quadrature is used.
"""
from __future__ import annotations

import itertools
import json
import platform
from pathlib import Path

import sympy as s

x, y, t, w, z, eta = s.symbols('x y t w z eta')
a, b, c, xi = s.symbols('a b c xi')
checks: list[str] = []


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def equal(name: str, left: s.Expr, right: s.Expr = s.S.Zero) -> None:
    check(name, s.cancel(s.expand(left - right)) == 0)


def factorial_functional(f: s.Expr) -> s.Expr:
    return s.expand(sum(coef * s.factorial(i) * s.factorial(j)
                        for (i, j), coef in s.Poly(f, x, y).terms()))


def main() -> None:
    # Root-of-unity filter checked in the exact cyclotomic quotient.
    for degree in range(1, 7):
        cyclo = s.cyclotomic_poly(degree, z)
        for power in range(-1, 5 * degree + 1):
            trace = sum(z ** ((k * power) % degree) for k in range(degree))
            trace = s.rem(trace, cyclo, z)
            coefficient = trace / (degree * s.factorial(power + 1))
            if degree == 1 and power == -1:
                coefficient -= 1
            target = (1 / s.factorial(power + 1)
                      if power >= 0 and power % degree == 0 else s.S.Zero)
            equal(f'root filter D={degree}, power={power}', coefficient, target)

    # Direct monomial factorial evaluation versus the radial-projective integral.
    r = s.symbols('r')
    polynomials = [x**2 + x*y + 2*y + 1,
                   x**3 - 2*x*y + y**2 + 3,
                   (x+y)**4 + x**2*y + x - 2*y + 1]
    for index, f in enumerate(polynomials, 1):
        for n in range(5):
            radial = s.Poly(s.expand(f.subs({x:r*t, y:r*(1-t)})**n), r)
            angular = sum(s.factorial(k[0]+1)*coef for k, coef in radial.terms())
            radial_value = s.integrate(angular, (t, 0, 1))
            equal(f'radial/factorial identity family={index}, n={n}',
                  radial_value, factorial_functional(s.expand(f**n)))

    # The exact coefficient majorant used for uniform dominated convergence.
    for degree in range(1, 5):
        for n in range(1, 5):
            for ks in itertools.product(range(n+1), repeat=degree):
                K = sum(ks)
                if K > n:
                    continue
                J = sum((j+1)*kj for j, kj in enumerate(ks))
                coefficient = (s.factorial(n)/s.factorial(n-K)
                               *s.factorial(degree*n-J+1)/s.factorial(degree*n+1))
                check(f'radial bound D={degree}, n={n}, k={ks}',
                      bool(0 <= coefficient <= 1))

    # Exact shifted-square comparison, in independent local variables 1/Y and eta.
    # The p=0 family checks the displayed quadratic coefficient; p!=0 also
    # checks the next homogeneous layer.
    for p, q in [(0, 3), (2, 3)]:
        root = s.sqrt(1-q*z**2)
        F_scaled = s.series(s.exp((1-root)/z)*(1-p*z/root), z, 0, 7).removeO()
        from_reversion = sum((-1)**m * s.expand(F_scaled).coeff(z,m)
                              *eta**(m-1)/s.factorial(m-1) for m in range(1,7))
        v = q*((1-eta)**2-1)/4
        S0 = sum(v**j/s.factorial(j)**2 for j in range(7))
        S1 = sum(v**j/(s.factorial(j)*s.factorial(j+1)) for j in range(7))
        from_beta = s.series(p*S0 - s.Rational(q,2)*S1, eta, 0, 6).removeO()
        for j in range(6):
            equal(f'quadratic coefficient p={p}, q={q}, eta power={j}',
                  s.expand(from_reversion).coeff(eta,j),
                  s.expand(from_beta).coeff(eta,j))

    # Perfect-power differential and the retained-history expression.
    L, sv, Lp = a*t+b, s.symbols('s', nonzero=True), s.symbols('Lp', nonzero=True)
    for degree in range(2,6):
        B = c*s.exp(c/L)/(degree*L**2*sv**(degree-1))
        exact = -s.diff(s.exp(c/L), t)/(degree*a*sv**(degree-1))
        equal(f'perfect-power differential D={degree}', B, exact)
        pole = s.exp(c/sv)/(degree*a*sv**(degree-1))
        correction = -(s.exp(c/sv)-s.exp(c/Lp))/(degree*a*sv**(degree-1))
        equal(f'perfect-power corrected germ D={degree}',
              pole+correction, s.exp(c/Lp)/(degree*a*sv**(degree-1)))

    # Finite algebra quotient calculation for the weighted density system.
    A, Bpoly, degree = t**2+1, t, 2
    modulus = s.Poly(A-w, t, domain=s.QQ.frac_field(w))
    inv = s.invert(s.Poly(s.diff(A,t),t,domain=s.QQ.frac_field(w)),modulus).as_expr()
    expected = s.Matrix([[-1/(2*(w-1)), (2-w)/(4*w**2*(w-1))],
                         [(2-w)/(4*w**2),0]])
    obtained = s.zeros(2)
    for j in range(2):
        expr = ((j*t**(j-1)*inv if j else 0)
                -t**j*s.diff(A,t,2)*inv**2
                +t**j*s.diff(Bpoly,t)*inv/(degree*w)
                -t**j*Bpoly/(degree*w**2))
        rem = s.Poly(expr,t,domain=s.QQ.frac_field(w)).rem(modulus)
        for k in range(2):
            obtained[j,k] = rem.nth(k)
            equal(f'density rational connection entry {j},{k}',obtained[j,k],expected[j,k])
    qden = 4*w**2*(w-1)
    check('density-system degree budget n=3',
          all(s.denom(s.cancel(qden*entry)) == 1
              and s.degree(s.cancel(qden*entry),w) <= 2 for entry in obtained))

    # Block trace: matrix trace of multiplication by 1/R' in Q(xi)[t]/(R-xi).
    for index, R in enumerate([t**2+t, t**3-2*t+1, t**4+t**2+3*t],1):
        mod = s.Poly(R-xi,t,domain=s.QQ.frac_field(xi))
        rinv = s.invert(s.Poly(s.diff(R,t),t,domain=s.QQ.frac_field(xi)),mod)
        d = s.degree(R,t)
        trace = sum((rinv*s.Poly(t**j,t,domain=s.QQ.frac_field(xi))).rem(mod).nth(j)
                    for j in range(d))
        equal(f'zero block trace family {index}', trace)

    # The exact full-system observation determinant for a linear polynomial.
    qlin = (w-a)*(w-b)
    M = s.Matrix([[0,-1/qlin,0],[0,-c/w**2,0],[0,0,0]])
    ell0 = s.Matrix([[1,0,-1/w]])
    ell1 = ell0.diff(w)+ell0*M
    ell2 = ell1.diff(w)+ell1*M
    determinant = ell0.col_join(ell1).col_join(ell2).det()
    numerator = -(a+b+c)*w**2+(2*a*b+c*(a+b))*w-c*a*b
    equal('linear observation determinant', determinant,numerator/(qlin**2*w**4))
    equal('linear degeneracy middle coefficient',
          (2*a*b+c*(a+b)).subs(c,-a-b), -a**2-b**2)

    # Elementary singular identities retain the sign of the logarithmic correction.
    zz = s.symbols('zz')
    equal('exact differential local cancellation',
          s.diff(s.sqrt(x)*s.log(zz-x),x),
          -s.sqrt(x)/(zz-x)+s.log(zz-x)/(2*s.sqrt(x)))

    result = {
        'purpose': 'Finite exact identities supporting factorial_conjecture_two_variables.tex; not formal verification of FC(2).',
        'python': platform.python_version(), 'sympy': s.__version__,
        'check_count': len(checks), 'passed_checks': checks,
    }
    output = Path(__file__).resolve().parents[1] / 'verification' / 'identities.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'{len(checks)} exact identity checks passed; wrote {output}')


if __name__ == '__main__':
    main()
