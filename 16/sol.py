import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return [list(line) for line in lines]


dirs = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}


mirrors = {'.': {d: [d] for d in dirs},
           '/': {'N': ['E'], 'S': ['W'], 'E': ['N'], 'W': ['S']},
           '\\': {'N': ['W'], 'S': ['E'], 'E': ['S'], 'W': ['N']},
           '|': {'N': ['N'], 'S': ['S'], 'E': ['N', 'S'], 'W': ['N', 'S']},
           '-': {'N': ['E', 'W'], 'S': ['E', 'W'], 'E': ['E'], 'W': ['W']}}


def solve1(grid, start=((0, 0), 'E')):
    rows, cols = len(grid), len(grid[0])
    beams = {start}
    vstd = set(beams)
    while beams:
        new_beams = set()
        for (r, c), d in beams:
            for e in mirrors[grid[r][c]][d]:
                dr, dc = dirs[e]
                if 0 <= (nr := r+dr) < rows and 0 <= (nc := c+dc) < cols and (new := ((nr, nc), e)) not in vstd:
                    new_beams.add(new)
        beams = new_beams
        vstd |= beams
    return len({c for c, _ in vstd})


def solve2(grid):
    rows, cols = len(grid), len(grid[0])
    def gen():
        for r in range(rows):
            yield ((r, 0), 'E')
            yield ((r, cols-1), 'W')
        for c in range(cols):
            yield ((0, c), 'S')
            yield ((rows-1, c), 'N')
    return max(solve1(grid, start) for start in gen())


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
