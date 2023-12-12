import sys
from itertools import product


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return [list(line) for line in lines]


dirs = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}


char_dirs = {'|': {dirs['N'], dirs['S']},
             '-': {dirs['E'], dirs['W']},
             'L': {dirs['N'], dirs['E']},
             'J': {dirs['N'], dirs['W']},
             '7': {dirs['S'], dirs['W']},
             'F': {dirs['S'], dirs['E']}}


def get_conn(chars, crd):
    try:
        r, c = crd
        return set((r+dr, c+dc) for dr, dc in char_dirs[chars[r][c]])
    except (IndexError, KeyError):
        return set()


def get_start(chars):
    start = None
    for r, c in product(range(len(chars)), range(len(chars[0]))):
        if chars[r][c] == "S":
            start = (r, c)
    assert start is not None, "No start found"

    conns = set()
    for dr, dc in dirs.values():
        if start in get_conn(chars, new := (start[0]+dr, start[1]+dc)):
            conns.add(new)
    assert len(conns) == 2, "Not exactly two connections"

    return start, conns


def get_next(chars, fr, to):
    s = get_conn(chars, to)
    s.remove(fr)
    return s.pop()


def solve1(chars):
    start, conns = get_start(chars)
    frs = [start, start]
    tos = list(conns)
    rtn = 1
    while tos[0] != tos[1]:
        nxs = [get_next(chars, fr, to) for fr, to in zip(frs, tos)]
        frs, tos = tos, nxs
        rtn += 1
    return rtn


def get_pipe(chars, start, conns):
    pipe = {start} | conns
    frs = [start, start]
    tos = list(conns)
    while tos[0] != tos[1]:
        nxs = [get_next(chars, fr, to) for fr, to in zip(frs, tos)]
        frs, tos = tos, nxs
        pipe |= set(tos)
    return pipe


def set_str(outside, pipe):
    def char(crd):
        if crd in outside:
            return "O"
        elif crd in pipe:
            return "#"
        else:
            return "I"
    mr = max(r for (r, _), _ in outside | pipe)
    mc = max(c for _, (c, _) in outside | pipe)
    rtn = ""
    for r in range(mr+1):
        for i in range(3):
            for c in range(mc+1):
                for j in range(3):
                    rtn += char(((r, i), (c, j)))
                rtn += " "
            rtn += "\n"
        rtn += "\n"
    return rtn


def solve2_9dots(chars):
    """
    Expand each character into a 3x3 grid.
    The pipe runs through the middle of the grid.
    The flood fill then seeps through the space not filled by the pipe.
    """
    start, conns = get_start(chars)
    # MUTATES CHARS
    chars[start[0]][start[1]] = {k for k, v in char_dirs.items() if v == {(r-start[0], c-start[1]) for r, c in conns}}.pop()
    pipe = get_pipe(chars, start, conns)

    char_subs = {'|': {(0, 1), (1, 1), (2, 1)},
                 '-': {(1, 0), (1, 1), (1, 2)},
                 'L': {(0, 1), (1, 1), (1, 2)},
                 'J': {(0, 1), (1, 1), (1, 0)},
                 '7': {(1, 0), (1, 1), (2, 1)},
                 'F': {(1, 2), (1, 1), (2, 1)}}
    pipe_sub = {((r, sr), (c, sc)) for r, c in pipe for sr, sc in char_subs[chars[r][c]]}

    mr, mc = len(chars), len(chars[0])
    def neighbors(crd):
        for dsr, dsc in dirs.values():
            (r, sr), (c, sc) = crd
            dr, sr = divmod(sr+dsr, 3)
            dc, sc = divmod(sc+dsc, 3)
            r += dr
            c += dc
            if 0 <= r < mr and 0 <= c < mc:
                yield ((r, sr), (c, sc))

    def edges():
        for c in range(mc):
            for i in range(3):
                yield ((0, 0), (c, i))
                yield ((mr-1, 2), (c, i))
        for r in range(mr):
            for i in range(3):
                yield ((r, i), (0, 0))
                yield ((r, i), (mc-1, 2))
    stack = list(edges())
    outside = set()
    while stack:
        crd = stack.pop()
        if crd not in outside and crd not in pipe_sub:
            outside.add(crd)
            for new in neighbors(crd):
                stack.append(new)
    # print(set_str(outside, pipe_sub))

    # # remove all subpixels of the pipe
    # outside -= {((r,sr), (c,sc)) for r, c in pipe for sr, sc in product(range(3), range(3))}
    # assert len(outside) % 9 == 0, f"{len(outside)} % 0 == {len(outside) % 9}"
    # return mr * mc - (len(outside)//9) - len(pipe)

    # for r, c in product(range(mr), range(mc)):
    #     if (r, c) not in pipe:
    #         assert all((((r,i), (c,j)) in outside) == (((r,1), (c,1)) in outside) for i, j in product(range(3), range(3))), f"{r, c} inconsistent"
    return sum((r, c) not in pipe and ((r, 1), (c, 1)) not in outside for r, c in product(range(mr), range(mc)))


def solve2_new(chars):
    start, conns = get_start(chars)
    # MUTATES CHARS
    chars[start[0]][start[1]] = {k for k, v in char_dirs.items() if v == {(r-start[0], c-start[1]) for r, c in conns}}.pop()
    pipe = get_pipe(chars, start, conns)

    mr, mc = len(chars), len(chars[0])
    rtn = 0
    for r in range(mr):
        inside_up = False
        inside_dn = False
        for c in range(mc):
            if (r, c) in pipe:
                match chars[r][c]:
                    case '|':
                        inside_up = not inside_up
                        inside_dn = not inside_dn
                    case '-':
                        pass
                    case 'L':
                        inside_up = not inside_up
                    case 'J':
                        inside_up = not inside_up
                    case '7':
                        inside_dn = not inside_dn
                    case 'F':
                        inside_dn = not inside_dn
            else:
                assert inside_up == inside_dn, f"{r, c} up/down counts don't match"
                rtn += inside_up
    return rtn


solve2 = solve2_new


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
