import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    def parse_line(line):
        words = line.split()
        return words[0], int(words[1]), words[2][2:8]
    return [parse_line(line) for line in lines]


def area(insts):
    old_x, old_y = 0, 0
    interior = 0
    edge = 0
    for d, n in insts:
        match d:
            case 'U':
                new_x, new_y = old_x, old_y + n
            case 'D':
                new_x, new_y = old_x, old_y - n
            case 'L':
                new_x, new_y = old_x - n, old_y
            case 'R':
                new_x, new_y = old_x + n, old_y
        interior += old_x * new_y - old_y * new_x
        edge += abs(new_x - old_x) + abs(new_y - old_y)
        old_x, old_y = new_x, new_y
    assert old_x == 0 and old_y == 0
    return abs(interior)//2 + edge//2 + 1


def solve1(x):
    return area((d, n) for d, n, _ in x)


def solve2(x):
    dirs = ['R', 'D', 'L', 'U']
    def convert(c):
        return dirs[int(c[-1])], int(c[:5], 16)
    return area(convert(c) for _, _, c in x)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
