import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return [tuple(tuple(int(n) for n in s.split(',')) for s in line.split('~')) for line in lines]


def make_arr(bricks):
    ms = [max(c[i]+1 for _, c in bricks) for i in range(3)]
    arr = [[[False for _ in range(ms[2])] for _ in range(ms[1])] for _ in range(ms[0])]
    for x in range(ms[0]):
        for y in range(ms[1]):
            arr[x][y][0] = True
    for i, a in bricks:
        ix, iy, iz = i
        ax, ay, az = a
        for x in range(ix, ax+1):
            for y in range(iy, ay+1):
                for z in range(iz, az+1):
                    arr[x][y][z] = True
    return arr


def fall(bricks):
    # MUTATES bricks
    arr = make_arr(bricks)
    changed = True
    while changed:
        changed = False
        for idx, brick in enumerate(bricks):
            (ix, iy, iz), (ax, ay, az) = brick
            dz = az - iz + 1
            rx, ry, rz = range(ix, ax+1), range(iy, ay+1), range(iz, az+1)
            if any(arr[x][y][iz-1] for x in rx for y in ry):
                continue
            for mz in reversed(range(iz)):
                if any(arr[x][y][mz] for x in rx for y in ry):
                    break
            for x in rx:
                for y in ry:
                    for z in rz:
                        arr[x][y][z] = False
            for x in rx:
                for y in ry:
                    for z in range(mz+1, mz+1+dz):
                        arr[x][y][z] = True
            bricks[idx] = ((ix, iy, mz+1), (ax, ay, mz+dz))
            changed = True


def succs(bricks):
    rtn = [set() for _ in range(len(bricks))]
    for i, brick in enumerate(bricks):
        (ix, iy, iz), (ax, ay, az) = brick
        for j, other in enumerate(bricks):
            if i == j:
                continue
            (jx, jy, jz), (bx, by, bz) = other
            if bz == iz-1 and ix <= bx and jx <= ax and iy <= by and jy <= ay:
                rtn[i].add(j)
    return rtn


def solve1(x):
    s = succs(x)
    return len(x) - len(set().union(*(t for t in s if len(t) == 1)))
    # return len(x) - len({i for t in s for i in t if len(t) == 1})
    # return sum(not any(t == {i} for t in s) for i in range(len(x)))


def paths_down(succ, i):
    if not succ[i]:
        return [{i}]
    return [{i} | p for j in succ[i] for p in paths_down(succ, j)]


def solve2(x):
    s = succs(x)
    paths = [paths_down(s, i) for i in range(len(x))]
    return sum(sum(i != j and all(i in p for p in paths[j]) for j in range(len(x))) for i in range(len(x)))

if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    fall(x)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
