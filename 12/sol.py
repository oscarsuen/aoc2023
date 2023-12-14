import sys
from functools import cache


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    def parse_line(line):
        words = line.split()
        assert len(words) == 2, f"Invalid line: {line}"
        return words[0], tuple(int(num) for num in words[1].split(","))
    return [parse_line(line) for line in lines]


def matches_old(line, vals):
    before, sep, after = line.partition('?')
    if not sep:
        return tuple(len(run) for run in line.split('.') if run) == vals
    new_dot = before + '.' + after
    new_hash = before + '#' + after
    return matches_old(new_dot, vals) + matches_old(new_hash, vals)


def matches_new(line, vals):
    rtn = 0
    n = len(line) - sum(vals)
    k = len(vals)
    def next_part(a, i):
        while i >= 0 and a[i] >= n - sum(a[:i]) - (k-i-1):
            i -= 1
        if i < 0:
            raise StopIteration
        a[i] += 1
        a[i+1:] = [1]*(k-i-1)
    @cache
    def run_char(i, j, hash):
        return all(c == ('#' if hash else '.') or c == '?' for c in line[i:j])
    run = [0] + [1]*(k-1)
    while True:
        curr = 0
        for i in range(len(vals)):
            if not run_char(curr, curr+run[i], False):
                break
            curr += run[i]
            if not run_char(curr, curr+vals[i], True):
                break
            curr += vals[i]
        else:
            if run_char(curr, len(line), False):
                rtn += 1
        try:
            next_part(run, i)
        except StopIteration:
            break
    return rtn


@cache
def matches_dp(line, vals):
    if not vals:
        return '#' not in line
    mi = min(len(line) - sum(vals) - len(vals) + 2, len(line) - vals[0] + 1)
    rtn = 0
    for i in range(mi):
        j = i + vals[0]
        if '.' not in line[i:j] and line[j:j+1] != '#':
            rtn += matches_dp(line[j+1:], vals[1:])
        if line[i:i+1] == '#':
            break
    return rtn


matches = matches_dp


def solve1(x):
    return sum(matches(rec, vals) for rec, vals in x)


def solve2(x, folds=5):
    return sum(matches('?'.join(rec for _ in range(folds)), vals*folds) for rec, vals in x)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
