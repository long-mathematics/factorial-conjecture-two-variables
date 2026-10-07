#!/usr/bin/env python3
"""Exact degree-six collision checks using only the Python standard library.

Arithmetic is in Q(sqrt(3)); no numerical root tracking is used.
"""
from fractions import Fraction as F
from pathlib import Path
import json


class Q3:
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q3) else Q3(x)
    def __add__(self, other):
        o = self.coerce(other)
        return Q3(self.a+o.a, self.b+o.b)
    __radd__ = __add__
    def __neg__(self):
        return Q3(-self.a, -self.b)
    def __sub__(self, other):
        return self + -self.coerce(other)
    def __rsub__(self, other):
        return self.coerce(other) + -self
    def __mul__(self, other):
        o = self.coerce(other)
        return Q3(self.a*o.a+3*self.b*o.b, self.a*o.b+self.b*o.a)
    __rmul__ = __mul__
    def __eq__(self, other):
        o = self.coerce(other)
        return self.a == o.a and self.b == o.b
    def pair(self):
        return [str(self.a), str(self.b)]


def add(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else F(0))
            + (q[i] if i < len(q) else F(0)) for i in range(n)]


def mul(p, q):
    out = [F(0)]*(len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return out


def compose(p, q):
    out = [F(0)]
    for a in reversed(p):
        out = add(mul(out, q), [a])
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def derivative(p):
    return [i*p[i] for i in range(1, len(p))]


def evaluate(p, x):
    out = Q3()
    for a in reversed(p):
        out = out*x + a
    return out


def main():
    t2 = list(map(F, [-1, 0, 2]))
    t3 = list(map(F, [0, -3, 0, 4]))
    t6 = list(map(F, [-1, 0, 18, 0, -48, 0, 32]))
    checks = []
    def check(name, condition):
        assert condition, name
        checks.append(name)
    check('T6 = T2 composed with T3', compose(t2, t3) == t6)
    check('T6 = T3 composed with T2', compose(t3, t2) == t6)
    affine = [F(-1), F(2)]
    a = compose(t6, affine)
    a[0] -= 1
    r3 = compose(t3, affine)
    check('A+2 = 2 R3^2', add(a, [F(2)]) == [2*x for x in mul(r3, r3)])
    ap, app = derivative(a), derivative(derivative(a))
    check('A(0)=A(1)=0', evaluate(a, Q3(0)) == 0 and evaluate(a, Q3(1)) == 0)
    check('A prime at endpoints = -72,+72', evaluate(ap, Q3(0)) == -72 and evaluate(ap, Q3(1)) == 72)
    points = [Q3(F(1,2), F(-1,4)), Q3(F(1,2)), Q3(F(1,2), F(1,4))]
    local_a = [F(288), F(72), F(288)]
    weights = []
    for j, (c, ac) in enumerate(zip(points, local_a), 1):
        check(f'A(c{j})=-2', evaluate(a, c) == -2)
        check(f'A prime(c{j})=0', evaluate(ap, c) == 0)
        check(f'A double-prime(c{j})/2={ac}', evaluate(app, c) == 2*ac)
        weights.append(F(1, 2*ac))
    check('critical-point weights have ratio 1:4:1', [576*x for x in weights] == [1, 4, 1])
    for c in [F(1,4), F(3,4)]:
        check(f'other critical point {c} maps to zero', evaluate(a, Q3(c)) == 0 and evaluate(ap, Q3(c)) == 0)
    result = {
        'arithmetic': 'Exact rational arithmetic in Q(sqrt(3)); pairs mean a+b sqrt(3)',
        'polynomial_coefficients_ascending': [str(x) for x in a],
        'nonzero_critical_value': '-2',
        'critical_points': [c.pair() for c in points],
        'local_quadratic_coefficients': [str(x) for x in local_a],
        'positive_critical_point_weights': [str(x) for x in weights],
        'weight_ratio': [1, 4, 1],
        'passed_checks': checks,
        'check_count': len(checks),
    }
    path = Path(__file__).resolve().parents[1] / 'verification' / 'degree6.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(f'{len(checks)} exact checks passed; wrote {path}')


if __name__ == '__main__':
    main()
