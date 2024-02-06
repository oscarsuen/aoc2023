import sys
from math import prod


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    grid = []
    origin = None
    for r, line in enumerate(lines):
        add = []
        for c, x in enumerate(line):
            match x:
                case ".":
                    add.append(True)
                case "#":
                    add.append(False)
                case "S":
                    add.append(True)
                    origin = (r, c)
        grid.append(add)
    return grid, origin


def grid_dist(grid, origin):
    rows, cols = len(grid), len(grid[0])
    dist = [[None for _ in range(cols)] for _ in range(rows)]
    dist[origin[0]][origin[1]] = 0
    curr = {origin}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    def neighbors(r, c):
        for dr, dc in dirs:
            if 0 <= (nr := r+dr) < rows and 0 <= (nc := c+dc) < cols:
                yield nr, nc
    while curr:
        new = set()
        for r, c in curr:
            for nr, nc in neighbors(r, c):
                if grid[nr][nc] and dist[nr][nc] is None:
                    dist[nr][nc] = dist[r][c] + 1
                    new.add((nr, nc))
        curr = new
    return dist


def dist_gen(dist):
    rows, cols = len(dist), len(dist[0])
    for r in range(rows):
        for c in range(cols):
            if dist[r][c] is not None:
                yield r, c


def dist_count(dist, n=None, parity=None):
    rows, cols = len(dist), len(dist[0])
    if n is None:
        # n = max(max(row) for row in dist)
        n = rows*cols
    if parity is None:
        parity = n % 2
    return sum(dist[r][c] <= n and dist[r][c] % 2 == parity for r, c in dist_gen(dist))


def solve1(x, n=64):
    grid, origin = x
    # dist = grid_dist(grid, origin)
    # return dist_count(dist, n)
    curr = {origin}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(grid), len(grid[0])
    def neighbors(r, c):
        for dr, dc in dirs:
            if 0 <= (nr := r+dr) < rows and 0 <= (nc := c+dc) < cols:
                yield nr, nc
    for _ in range(n):
        new = set()
        for r, c in curr:
            for nr, nc in neighbors(r, c):
                if grid[nr][nc]:
                    new.add((nr, nc))
        curr = new
    return len(curr)


def solve2_direct(x, n=26501365):
    grid, origin = x
    curr = {origin}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(grid), len(grid[0])
    def neighbors(r, c):
        for dr, dc in dirs:
            yield r+dr, c+dc
    for _ in range(n):
        new = set()
        for r, c in curr:
            for nr, nc in neighbors(r, c):
                if grid[nr % rows][nc % cols]:
                    new.add((nr, nc))
        curr = new
    return len(curr)


def solve2_calc(x, n=26501365):
    grid, origin = x
    rows, cols = len(grid), len(grid[0])
    assert rows == cols
    assert rows % 2 == 1
    assert all(grid[r][0] for r in range(rows)) and \
        all(grid[r][cols-1] for r in range(rows)) and \
        all(grid[0][c] for c in range(cols)) and \
        all(grid[rows-1][c] for c in range(cols))
    assert origin[0] == rows//2 and origin[1] == cols//2
    assert all(grid[origin[0]][c] for c in range(cols)) and \
        all(grid[r][origin[1]] for r in range(rows))

    div, mod = divmod(n, rows)
    assert div > 1

    d_origin = grid_dist(grid, origin)
    even = dist_count(d_origin, parity=n%2)
    odd = dist_count(d_origin, parity=1-n%2)

    even_bks = (div-(1-div%2))**2
    odd_bks = (div-(div%2))**2

    partial = 0

    corners = [(0, 0), (0, cols-1), (rows-1, cols-1), (rows-1, 0)]
    for crd in corners:
        d = grid_dist(grid, crd)
        far = dist_count(d, mod, (1-div%2)^(n%2))
        partial += far*div
        near = dist_count(d, mod+rows, (div%2)^(n%2))
        partial += near*(div-1)

    sides = [(0, origin[1]), (origin[0], cols-1), (rows-1, origin[1]), (origin[0], 0)]
    for crd in sides:
        d = grid_dist(grid, crd)
        partial += dist_count(d, mod+rows//2, (1-div%2)^(n%2))

    return even_bks * even + odd_bks * odd + partial


def solve2_interp(x, n=26501365):
    grid, origin = x
    rows, cols = len(grid), len(grid[0])
    assert rows == cols
    div, mod = divmod(n, rows)
    c = solve2_direct(x, mod)
    a_b_c = solve2_direct(x, mod+rows)
    a4_b2_c = solve2_direct(x, mod+2*rows)
    a = (a4_b2_c - 2*a_b_c + c) // 2
    b = a_b_c - a - c
    return a*div**2 + b*div + c


solve2 = solve2_calc


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
