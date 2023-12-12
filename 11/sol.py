import sys
from itertools import product, combinations


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    grid = [list(line) for line in input_string.split("\n")]
    mr, mc = len(grid), len(grid[0])
    rows = [all(grid[r][c] == "." for c in range(mc)) for r in range(mr)]
    cols = [all(grid[r][c] == "." for r in range(mr)) for c in range(mc)]
    galaxies = {(r, c) for r, c in product(range(mr), range(mc)) if grid[r][c] == "#"}
    return rows, cols, galaxies


def dist(g1, g2, rows, cols, expansion=2):
    r1, c1 = g1
    r2, c2 = g2
    rmin, rmax = min(r1, r2), max(r1, r2)
    cmin, cmax = min(c1, c2), max(c1, c2)
    return sum((not b)+b*expansion for b in rows[rmin:rmax]) + sum((not b)+b*expansion for b in cols[cmin:cmax])


def solve1(x):
    rows, cols, galaxies = x
    return sum(dist(g1, g2, rows, cols) for g1, g2 in combinations(galaxies, 2))


def solve2(x, exp=1000000):
    rows, cols, galaxies = x
    return sum(dist(g1, g2, rows, cols, exp) for g1, g2 in combinations(galaxies, 2))


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
