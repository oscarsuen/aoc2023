import sys
from itertools import combinations
from fractions import Fraction
from random import gauss, uniform, sample
from math import gcd


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return [tuple(tuple(int(n) for n in c.split(", ")) for c in line.split(" @ ")) for line in lines]


def linalgsolve2x2(mat, vec):
    # solve Ax = b for 2x2 matrix A and 2-vector b
    ((a, b), (c, d)) = mat
    (x, y) = vec
    det = a * d - b * c
    if det == 0:
        return None
    return (Fraction(d * x - b * y, det),
            Fraction(-c * x + a * y, det))


def point(p, v, t):
    # p + tv
    # assert len(p) == len(v)
    return tuple(pi + vi * t for pi, vi in zip(p, v))


def solve1(eqs, xymin=200000000000000, xymax=400000000000000):
    def intersection(l1, l2):
        (px1, py1, _), (vx1, vy1, _) = l1
        (px2, py2, _), (vx2, vy2, _) = l2
        # solve for t1, t2 such that p1 + t1 v1 = p2 + t2 v2
        # t1 v1 - t2 v2 = p2 - p1
        # [v1, -v2] [t1, t2]^T = p2 - p1
        mat = ((vx1, -vx2), (vy1, -vy2))
        vec = (px2 - px1, py2 - py1)
        return linalgsolve2x2(mat, vec)
    def test(l1, l2):
        t = intersection(l1, l2)
        if t is None:
            return False
        if any(ti < 0 for ti in t):
            return False
        t1, _ = t
        p = point(*l1, t1)
        return all(xymin <= pi <= xymax for pi in p[:2])
    return sum(test(l1, l2) for l1, l2 in combinations(eqs, 2))


def diff(v, w):
    # difference between two vectors
    return tuple(vi - wi for vi, wi in zip(v, w))


def scale(v, s):
    # scale vector by scalar
    return tuple(s * vi for vi in v)


def dot(v, w):
    # 3D dot product
    return sum(vi * wi for vi, wi in zip(v, w))


def cross(v, w):
    # 3D cross product
    return (v[1] * w[2] - v[2] * w[1],
            v[2] * w[0] - v[0] * w[2],
            v[0] * w[1] - v[1] * w[0])


def matvec(mat, vec):
    # matrix-vector product
    return tuple(dot(row, vec) for row in mat)


def gauss_elim(mat, vec):
    aug = [row + (vi,) for row, vi in zip(mat, vec)]
    d = len(aug)
    for i in range(d):
        if aug[i][i] == 0:
            j = i
            while j < d:
                if aug[j][i] != 0:
                    break
                j += 1
            else:
                return None
            aug[i], aug[j] = aug[j], aug[i]
        aug[i] = scale(aug[i], Fraction(1, aug[i][i]))
        for j in range(i+1, d):
            aug[j] = diff(aug[j], scale(aug[i], aug[j][i]))
    for i in reversed(range(d)):
        for j in reversed(range(i)):
            aug[j] = diff(aug[j], scale(aug[i], aug[j][i]))
    identity = [tuple(i == j for j in range(d)) for i in range(d)]
    assert [row[:-1] for row in aug] == identity
    return tuple(row[-1] for row in aug)


def solve2(eqs):
    def xmat(w):
        # derivative of 3D cross product
        return ((0, w[2], -w[1]),
                (-w[2], 0, w[0]),
                (w[1], -w[0], 0))
    def linsys(l1, l2, l3):
        (p1, v1), (p2, v2), (p3, v3) = l1, l2, l3
        # solve for q, w \in Z^3, t \in N^n or Q^n
        # pi + vi ti == q + w ti
        # (pi - q) \times (vi - w) == 0
        # q \times (vi - vj) + (pi - pj) \times w == pi \times vi - pj \times vj
        dv1 = diff(v1, v2)
        dp1 = diff(p1, p2)
        db1 = diff(cross(p1, v1), cross(p2, v2))
        dv2 = diff(v2, v3)
        dp2 = diff(p2, p3)
        db2 = diff(cross(p2, v2), cross(p3, v3))
        mat = tuple(a+b for a, b in zip(xmat(dv1), xmat(dp1))) + \
            tuple(a+b for a, b in zip(xmat(dv2), xmat(dp2)))
        vec = db1 + db2
        return mat, vec
    while True:
        l1, l2, l3 = sample(eqs, 3)
        mat, vec = linsys(l1, l2, l3)
        sol = gauss_elim(mat, vec)
        if sol is None:
            continue
        if any(si.denominator != 1 for si in sol):
            continue
        # print(tuple(si.numerator for si in sol))
        return sum(si.numerator for si in sol[:3])


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
