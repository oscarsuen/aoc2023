import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return tuple(tuple(line) for line in lines)


def solve1(grid):
    rows, cols = len(grid), len(grid[0])
    dirs = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    stack = [((0, c), {(0, c)}) for c in range(cols) if grid[0][c] == '.']
    rtn = []
    while stack:
        (r, c), visited = stack.pop()
        if r == rows - 1:
            rtn.append(len(visited)-1)
            continue
        ds = dirs.values() if (h := grid[r][c]) == '.' else [dirs[h]]
        for dr, dc in ds:
            nr, nc = r + dr, c + dc
            if (n := (nr, nc)) not in visited and 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                stack.append((n, visited | {n}))
    return max(rtn)


def solve2_repeat(grid):
    rows, cols = len(grid), len(grid[0])
    dirs = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    stack = [((0, c), {(0, c)}) for c in range(cols) if grid[0][c] == '.']
    rtn = []
    while stack:
        (r, c), visited = stack.pop()
        if r == rows - 1:
            rtn.append(len(visited)-1)
            continue
        for dr, dc in dirs.values():
            nr, nc = r + dr, c + dc
            if (n := (nr, nc)) not in visited and 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                stack.append((n, visited | {n}))
    return max(rtn)


def solve2_graph(grid):
    rows, cols = len(grid), len(grid[0])
    dirs = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    for c in range(cols):
        if grid[0][c] == '.':
            break
    start = (0, c)
    for c in range(cols):
        if grid[rows-1][c] == '.':
            break
    end = (rows-1, c)
    nodes = {start: {}}
    seen = {start: set()}
    stack = [(start, dirs['v'], start, (1, start[1]), 1)]
    while stack:
        node, ndir, prev, curr, dist = stack.pop()
        r, c = curr
        ds = []
        for dr, dc in dirs.values():
            nr, nc = r + dr, c + dc
            if (n := (nr, nc)) != prev and 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                ds.append(n)
        if len(ds) == 1:
            stack.append((node, ndir, curr, ds[0], dist+1))
            continue
        # reached node
        assert node in nodes
        nodes[node][curr] = dist
        seen[node].add(ndir)
        nodes.setdefault(curr, {})[node] = dist
        pr, pc = prev
        dr, dc = pr-r, pc-c
        seen.setdefault(curr, set()).add((dr, dc))
        for nr, nc in ds:
            dr, dc = nr-r, nc-c
            if (dr, dc) not in seen[curr]:
                stack.append((curr, (dr, dc), curr, (nr, nc), 1))

    stack = [(start, {start}, 0)]
    rtn = []
    while stack:
        node, visited, dist = stack.pop()
        if node == end:
            rtn.append(dist)
            continue
        for new in nodes[node]:
            if new not in visited:
                stack.append((new, visited | {new}, dist + nodes[node][new]))
    return max(rtn)


solve2 = solve2_graph


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
