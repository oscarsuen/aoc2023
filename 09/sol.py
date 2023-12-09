import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    return [[int(x) for x in line.split()] for line in lines]


def solve1(x):
    def next_val(seq):
        if all(val == 0 for val in seq):
            return 0
        return seq[-1] + next_val([seq[i+1]-seq[i] for i in range(len(seq)-1)])
    return sum(next_val(seq) for seq in x)


def solve2(x):
    def prev_val(seq):
        if all(val == 0 for val in seq):
            return 0
        return seq[0] - prev_val([seq[i+1]-seq[i] for i in range(len(seq)-1)])
    return sum(prev_val(seq) for seq in x)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
