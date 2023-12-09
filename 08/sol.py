import sys
from math import lcm, gcd
from itertools import product


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


char_idxs = {'L': 0, 'R': 1}


def parse(input_string):
    lines = input_string.split("\n")
    def parse_line(line):
        src = line[0:3]
        lft = line[7:10]
        rgt = line[12:15]
        return (src, (lft, rgt))
    return [char_idxs[char] for char in lines[0]], dict(parse_line(line) for line in lines[2:])


def solve1(x, start="AAA", end="ZZZ"):
    inst, graph = x
    idx = 0
    curr = start
    rtn = 0
    while curr != end:
        curr = graph[curr][inst[idx]]
        idx = (idx + 1) % len(inst)
        rtn += 1
    return rtn


# This only works for specialized inputs like the one given
def solve2_special(x, start='A', end='Z'):
    inst, graph = x
    def solve(node):
        idx = 0
        curr = node
        rtn = 0
        while curr[-1] != end:
            curr = graph[curr][inst[idx]]
            idx = (idx + 1) % len(inst)
            rtn += 1
        return rtn
    return lcm(*(solve(node) for node in graph if node[-1] == start))


def bezout(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    assert old_r == gcd(a, b)
    return old_s, old_t
def crt(x, y):
    if x is None or y is None:
        return None
    a, m = x
    b, n = y
    if (a-b) % gcd(m, n) != 0:
        return None
    u, v = bezout(m, n)
    l = (a-b) // gcd(m, n)
    assert a-m*u*l == b+n*v*l
    s = a-m*u*l
    return s, lcm(m, n)
def fold_crt(*xs):
    r = (0, 1)
    for x in xs:
        r = crt(r, x)
    return r


def solve2(x, start='A', end='Z'):
    inst, graph = x
    def check_node(node):
        return node[-1] == end
    inst_idx = 0
    paths = [[(node, inst_idx)] for node in graph if node[-1] == start]
    vstds = [set(path) for path in paths]
    cycles = [None for _ in paths]
    # don't need idxs if we are just computing cycles
    idxs = [0 for _ in paths]
    # curr unnecessary
    curr = [path[idx][0] for path, idx in zip(paths, idxs)]
    rtn = 0
    while any(cycle is None for cycle in cycles) and any(not check_node(node) for node in curr):
        for i, (path, vstd, cycle, idx) in enumerate(zip(paths, vstds, cycles, idxs)):
            if cycle is None:
                new = graph[path[-1][0]][inst[inst_idx]]
                new = (new, (inst_idx+1) % len(inst))
                if new in vstd:
                    new_idx = path.index(new)
                    cycles[i] = new_idx
                else:
                    path.append(new)
                    vstd.add(new)
            idxs[i] = idx+1 if idx+1 < len(path) else cycles[i]
        curr = [path[idx][0] for path, idx in zip(paths, idxs)]
        inst_idx = (inst_idx + 1) % len(inst)
        rtn += 1
    if all(check_node(node) for node in curr):
        return rtn

    def get_idx(idx, pathlen, cycle):
        return cycle + (idx-cycle) % (pathlen-cycle) if idx > cycle else idx
    def check_idx(idx):
        for path, cycle in zip(paths, cycles):
            path_idx = get_idx(idx, len(path), cycle)
            node = path[path_idx][0]
            if not check_node(node):
                return False
        return True
    pathlens = [len(path) for path in paths]
    ends = [{i for i, (node, _) in enumerate(path) if node[-1]==end} for path in paths]
    assert all(end for end in ends), "One of the paths has no end"

    # removes all indices that are before the cycling
    precycles = set()
    for end, cycle in zip(ends, cycles):
        rem = {idx for idx in end if idx < cycle}
        end -= rem
        precycles |= rem
    # any index before cycling is just checked
    precycles = sorted(list(precycles))
    for idx in precycles:
        if check_idx(idx):
            return idx

    # any index inside the cycle can be repeated
    rtn = []
    max_cycles = max(cycles)
    def get_rtn(val):
        a, m = val
        # gets smallest number equivalent to a mod m that is greater than max(cycles)
        a = a % m
        d, b = divmod(max_cycles, m)
        return a + m*(d+(a<b))
    for end in product(*ends):
        val = fold_crt(*((idx, pathlen-cycle) for pathlen, cycle, idx in zip(pathlens, cycles, end)))
        if val is None:
            continue
        rtn.append(get_rtn(val))
    return min(rtn)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
