import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return lines


def solve1(x):
    def val(line):
        digs = [char for char in line if char.isdigit()]
        return int(digs[0]+digs[-1])
    return sum(val(line) for line in x)


def solve2(x):
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    def val(line):
        def fst(line, word):
            return idx if (idx := line.find(word)) != -1 else len(line)
        def lst(line, word):
            return idx if (idx := line.rfind(word)) != -1 else -1
        digs = [char for char in line if char.isdigit()]
        firsts = [line.index(digs[0])] + [fst(line, word) for word in words]
        lasts = [line.rindex(digs[-1])] + [lst(line, word) for word in words]
        first = str(fidx) if (fidx := firsts.index(min(firsts))) != 0 else line[firsts[0]]
        last = str(lidx) if (lidx := lasts.index(max(lasts))) != 0 else line[lasts[0]]
        return int(first+last)
    return sum(val(line) for line in x)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
