import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    def parse_line(line):
        words = line.split()
        # idx = words[1][:-1]
        bags = ' '.join(words[2:]).split(" | ")
        assert len(bags) == 2
        my_nums = set(int(num) for num in bags[0].split())
        win_nums = set(int(num) for num in bags[1].split())
        return my_nums, win_nums
    return [parse_line(line) for line in lines]


def solve1(x):
    return sum(2**(len(isc)-1) for my_nums, win_nums in x if (isc := my_nums & win_nums))


def solve2(x):
    cts = [1 for _ in x]
    matches = [len(my_nums & win_nums) for my_nums, win_nums in x]
    for i in range(len(x)):
        for j in range(i+1, i+1+matches[i]):
            cts[j] += cts[i]
    return sum(cts)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
