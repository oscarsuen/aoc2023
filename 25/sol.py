import sys
from math import ceil, sqrt
from random import choice, choices
from collections import Counter


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    rtn = {}
    for line in lines:
        node, neighbors = line.split(": ")
        for neighbor in neighbors.split():
            rtn.setdefault(node, set()).add(neighbor)
            rtn.setdefault(neighbor, set()).add(node)
    return rtn


def solve1(x):
    def random_edge(d):
        u = choices(list(d), weights=[c.total() for c in d.values()]).pop()
        v = choices(list(d[u]), weights=list(d[u].values())).pop()
        return u, v
    def merge(d, u, v):
        # assert u in d[v] and v in d[u]
        n = u | v
        c = d[u] + d[v]
        del c[u], c[v]
        del d[u], d[v]
        d[n] = c
        for neighbor in c:
            d[neighbor][n] = c[neighbor]
            d[neighbor].pop(u, None)
            d[neighbor].pop(v, None)
    def karger():
        d = {frozenset([node]): Counter(frozenset([n]) for n in neighbors) for node, neighbors in x.items()}
        # assert all(n not in d[n] for n in d)
        while len(d) > 2:
            u, v = random_edge(d)
            merge(d, u, v)
        a, b = d.keys()
        # assert len(d[a]) == len(d[b]) == 1
        # assert d[a][b] == d[b][a]
        return d[a][b], len(a) * len(b)
    while True:
        edges, rtn = karger()
        # print(edges, rtn)
        if edges == 3:
            return rtn


def solve2(x):
    pass


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
