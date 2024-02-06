import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    line = input_string.replace("\n", "")
    return line.split(",")


def hsh(s):
    rtn = 0
    for c in s:
        rtn += ord(c)
        rtn *= 17
        rtn %= 256
    return rtn


def solve1(x):
    return sum(hsh(s) for s in x)


def label(s):
    for i, c in enumerate(s):
        if c == '=' or c == '-':
            return s[:i], c, (int(s[i+1:]) if c == '=' else None)


def solve2(x):
    rtn = [[] for _ in range(256)]
    for s in x:
        b, c, i = label(s)
        lst = rtn[hsh(b)]
        match c:
            case '=':
                for j, (d, _) in enumerate(lst):
                    if b == d:
                        lst[j] = (b, i)
                        break
                else:
                    lst.append((b, i))
            case '-':
                k = None
                for j, (d, _) in enumerate(lst):
                    if b == d:
                        k = j
                        break
                if k is not None:
                    lst.pop(k)
    def score(i, lst):
        return (i+1) * sum((j+1)*k for j, (_, k) in enumerate(lst))
    return sum(score(i, lst) for i, lst in enumerate(rtn))


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
