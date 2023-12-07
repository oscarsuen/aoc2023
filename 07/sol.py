import sys
from collections import Counter


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    def parse_line(line):
        words = line.split()
        return tuple(words[0]), int(words[1])
    return [parse_line(line) for line in lines]


strength1 = {str(i): i for i in range(2, 10)}
strength1 |= {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

hands = {(1, 1, 1, 1, 1): 0,
         (2, 1, 1, 1): 1,
         (2, 2, 1): 2,
         (3, 1, 1): 3,
         (3, 2): 4,
         (4, 1): 5,
         (5,): 6}


def hand_type1(hand):
    ctr = Counter(hand)
    # return sorted(ctr.values(), reverse=True)
    return hands[tuple(sorted(ctr.values(), reverse=True))]


def solve1(x):
    std = sorted(x, key=lambda h: (hand_type1(h[0]),)+tuple(strength1[c] for c in h[0]))
    return sum(bid*(i+1) for i, (_, bid) in enumerate(std))


strength2 = {str(i): i for i in range(2, 10)}
strength2 |= {'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14}


def hand_type2(hand):
    ctr = Counter(hand)
    js = ctr.pop('J', 0)
    ctr[max(ctr, default='J', key=ctr.get)] += js
    # ctr[m[0][0] if (m := ctr.most_common()) else 'J'] += js
    return hands[tuple(sorted(ctr.values(), reverse=True))]


def solve2(x):
    std = sorted(x, key=lambda h: (hand_type2(h[0]),)+tuple(strength2[c] for c in h[0]))
    return sum(bid*(i+1) for i, (_, bid) in enumerate(std))


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
