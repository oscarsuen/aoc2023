import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    blocks = input_string.split("\n\n")
    def parse_block(block):
        rows = block.strip().splitlines()
        cols = [''.join(x) for x in zip(*rows)]
        return cols, rows
    return [parse_block(block) for block in blocks]


def refl(lst):
    rtn = set()
    for i in range(1, len(lst)):
        m = min(i, len(lst)-i)
        bef = lst[:i][-m:]
        aft = lst[i:][:m][::-1]
        if bef == aft:
            rtn.add(i)
    return rtn


def solve1(x):
    return sum(v.pop() if (v:=refl(cols)) else 100*refl(rows).pop() for cols, rows in x)


def solve2(x):
    def refl_smudge(x, y):
        refls = [refl(z) for z in y]
        poss = {i for i in range(1, len(x)) if sum(i in s for s in refls) == len(y)-1}
        rtn = set()
        for i in poss:
            m = min(i, len(x)-i)
            bef = x[:i][-m:]
            aft = x[i:][:m][::-1]
            if sum(b != a for b, a in zip(bef, aft)) == 1:
                rtn.add(i)
        return rtn
    return sum(v.pop() if (v:=refl_smudge(cols, rows)) else 100*refl_smudge(rows, cols).pop() for cols, rows in x)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
