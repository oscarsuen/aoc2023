import sys
import heapq


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return [[int(num) for num in line] for line in lines]


def dijkstra(grid, start, end, rng):
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    dist = [[[float("inf"), float("inf")] for _ in range(cols)] for _ in range(rows)]
    dist[sr][sc][False] = 0
    dist[sr][sc][True] = 0
    prev = [[[None, None] for _ in range(cols)] for _ in range(rows)]
    queue = []
    heapq.heappush(queue, (0, (sr, sc, False)))
    heapq.heappush(queue, (0, (sr, sc, True)))
    seen = {(sr, sc, False), (sr, sc, True)}
    def neighbors(ur, uc, d):
        def inbounds(r, c):
            return 0 <= r < rows and 0 <= c < cols
        if d:
            for i in rng:
                if inbounds(r := ur+i, c := uc):
                    yield (r, c, not d), sum(grid[ur+j][c] for j in range(1, i+1))
                if inbounds(r := ur-i, c := uc):
                    yield (r, c, not d), sum(grid[ur-j][c] for j in range(1, i+1))
        else:
            for i in rng:
                if inbounds(r := ur, c := uc+i):
                    yield (r, c, not d), sum(grid[r][uc+j] for j in range(1, i+1))
                if inbounds(r := ur, c := uc-i):
                    yield (r, c, not d), sum(grid[r][uc-j] for j in range(1, i+1))
    while queue:
        du, u = heapq.heappop(queue)
        seen.remove(u)
        # if u == end:
        #     break
        for (r, c, d), e in neighbors(*u):
            alt = du + e
            if alt < dist[r][c][d]:
                dist[r][c][d] = alt
                prev[r][c][d] = u
                if (r, c, d) in seen:
                    for i in range(len(queue)):
                        if queue[i][1] == (r, c, d):
                            queue[i] = (alt, (r, c, d))
                            heapq.heapify(queue)
                            break
                else:
                    heapq.heappush(queue, (alt, (r, c, d)))
                    seen.add((r, c, d))
    return dist, prev


def path(prev, start, end, d):
    curr = end + (d,)
    while curr[:2] != start:
        yield curr[:2]
        curr = prev[curr[0]][curr[1]][curr[2]]
    yield start[:2]


def solve1(grid):
    start = (0, 0)
    end = (len(grid)-1, len(grid[0])-1)
    dist, prev = dijkstra(grid, start, end, range(1, 4))
    return min(dist[end[0]][end[1]][False], dist[end[0]][end[1]][True])


def solve2(grid):
    start = (0, 0)
    end = (len(grid)-1, len(grid[0])-1)
    dist, prev = dijkstra(grid, start, end, range(4, 11))
    # print(list(path(prev, start, end, False)))
    # print(list(path(prev, start, end, True)))
    return min(dist[end[0]][end[1]][False], dist[end[0]][end[1]][True])


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
