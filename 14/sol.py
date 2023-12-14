import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return [list(line) for line in lines]


def grid_str(grid):
    return "\n".join("".join(row) for row in grid)


def score(grid):
    return sum(row.count('O')*(len(grid)-r) for r, row in enumerate(grid))


def solve1(grid):
    grid = [row.copy() for row in grid]
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'O':
                grid[r][c] = '.'
                s = r
                while s > 0 and grid[s-1][c] == '.':
                    s -= 1
                grid[s][c] = 'O'
    return score(grid)


def solve2(grid, cycles=1000000000):
    # MUTATES grid
    rows, cols = len(grid), len(grid[0])
    dirs = [('N', (-1, 0)), ('W', (0, -1)), ('S', (1, 0)), ('E', (0, 1))]
    def gen(dir):
        match dir:
            case 'N':
                for r in range(rows):
                    for c in range(cols):
                        yield r, c
            case 'W':
                for c in range(cols):
                    for r in range(rows):
                        yield r, c
            case 'S':
                for r in reversed(range(rows)):
                    for c in range(cols):
                        yield r, c
            case 'E':
                for c in reversed(range(cols)):
                    for r in range(rows):
                        yield r, c
    def next_char(r, c, dr, dc):
        return grid[r+dr][c+dc] if 0 <= r+dr < rows and 0 <= c+dc < cols else None
    hist = []
    vstd = set()
    while (gs := grid_str(grid)) not in vstd:
        hist.append(gs)
        vstd.add(gs)
        for dir, (dr, dc) in dirs:
            for r, c in gen(dir):
                if grid[r][c] == 'O':
                    grid[r][c] = '.'
                    s, d = r, c
                    while next_char(s, d, dr, dc) == '.':
                        s, d = s+dr, d+dc
                    grid[s][d] = 'O'
    cyc = hist.index(gs)
    mod = len(hist) - cyc
    idx = cyc + (cycles - cyc) % mod
    return score(parse(hist[idx]))


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
