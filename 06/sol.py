import sys
import math


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse1(input_string):
    lines = input_string.split("\n")
    assert len(lines) == 2
    return list(zip(*([int(num) for num in line.split()[1:]] for line in lines)))


def parse2(input_string):
    lines = input_string.split("\n")
    assert len(lines) == 2
    return tuple(int(''.join(line.split()[1:])) for line in lines)


def ans(time, dist):
    k1 = 0.5 * (time - math.sqrt(time**2 - 4*dist))
    k1 = int(k1+1) if k1.is_integer() else math.ceil(k1)
    k2 = 0.5 * (time + math.sqrt(time**2 - 4*dist))
    k2 = int(k2-1) if k2.is_integer() else math.floor(k2)
    return k2 - k1 + 1


def solve1(x):
    prod = 1
    for time, dist in x:
        prod *= ans(time, dist)
    return prod


def solve2(x):
    time, dist = x
    return ans(time, dist)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x1 = parse1(input_string)
    res1 = solve1(x1)
    print(f"Answer 1:\n{res1}\n")
    x2 = parse2(input_string)
    res2 = solve2(x2)
    print(f"Answer 2:\n{res2}\n")
