import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = [list(line) for line in input_string.split("\n")]
    return lines


def solve1(lines):
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]
    def gen():
        for row, line in enumerate(lines):
            curr_num = None
            yielded = False
            for col, char in enumerate(line):
                if char.isdigit():
                    if yielded:
                        continue
                    if curr_num is None:
                        j = col + 1
                        while j < len(line) and line[j].isdigit():
                            j += 1
                        curr_num = int(''.join(line[col:j]))
                    for dcol, drow in dirs:
                        try:
                            dchar = lines[row + drow][col + dcol]
                            if not dchar.isdigit() and dchar != ".":
                                yield curr_num
                                yielded = True
                                break
                        except IndexError:
                            pass
                else:
                    curr_num = None
                    yielded = False
    return sum(gen())


def solve2(x):
    lines = [line.copy() for line in x]
    vals = []
    for line in lines:
        curr_num = None
        for col, char in enumerate(line):
            if char == ".":
                line[col] = None
            if char.isdigit():
                if curr_num is None:
                    j = col + 1
                    while j < len(line) and line[j].isdigit():
                        j += 1
                    curr_num = int(''.join(line[col:j]))
                    vals.append(curr_num)
                line[col] = len(vals) - 1
            else:
                curr_num = None
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]
    def gen():
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == "*":
                    ptrs = set()
                    for dcol, drow in dirs:
                        try:
                            ptr = lines[row + drow][col + dcol]
                            if isinstance(ptr, int):
                                ptrs.add(ptr)
                        except IndexError:
                            pass
                    if len(ptrs) == 2:
                        yield vals[ptrs.pop()] * vals[ptrs.pop()]
    return sum(gen())


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
