import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    def parse_line(line):
        words = line.split()
        idx = int(words[1][:-1])
        draws = " ".join(words[2:]).split("; ")
        return idx, [{(sp := clause.split())[1]: int(sp[0]) for clause in draw.split(", ")} for draw in draws]
    return [parse_line(line) for line in lines]


def solve1(x):
    def possible(game, maxs={"red": 12, "green": 13, "blue": 14}):
        return all(k in maxs and maxs[k] >= v for draw in game for k, v in draw.items())
        # for draw in game:
        #     for k, v in draw.items():
        #         if k not in maxs or maxs[k] < v:
        #             return False
    return sum(idx for idx, game in x if possible(game))


def solve2(x):
    def power(game):
        colors = set().union(*game)
        maxs = {color: max(draw.get(color, 0) for draw in game) for color in colors}
        rtn = 1
        for color in colors:
            rtn *= maxs[color]
        return rtn
    return sum(power(game) for idx, game in x)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
