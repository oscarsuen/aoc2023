import sys
from itertools import product


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    workflows, parts = input_string.split("\n\n")
    def parse_wf(workflow):
        name, rules = workflow.split('{')  # }
        rules = rules[:-1].split(',')
        def parse_rule(rule):
            sp = rule.split(":")
            if len(sp) == 1:
                return None, sp[0]
            cond, key = sp
            for cmp in ['<', '>']:
                if cmp in cond:
                    cat, val = cond.split(cmp)
                    return (cat, cmp, int(val)), key
            raise ValueError(f"Invalid rule: {rule}")
        return name, [parse_rule(rule) for rule in rules]
    def parse_part(part):
        return {(s := clause.split('='))[0]: int(s[1]) for clause in part[1:-1].split(',')}
    return dict(parse_wf(wf) for wf in workflows.splitlines()), [parse_part(part) for part in parts.splitlines()]


def send(wf, part):
    for rule in wf:
        if rule[0] is None:
            return rule[1]
        cat, cmp, val = rule[0]
        if cmp == '<' and part[cat] < val:
            return rule[1]
        if cmp == '>' and part[cat] > val:
            return rule[1]
    return None


def accept(wfs, part, init="in"):
    curr = init
    while curr not in ["A", "R"]:
        curr = send(wfs[curr], part)
    return curr == "A"


def solve1(x):
    wfs, parts = x
    return sum(sum(part.values()) for part in parts if accept(wfs, part))


def solve2_old(x):
    wfs, _ = x
    cats = list("xmas")
    nums = {cat: [] for cat in cats}
    for _, wf in wfs.items():
        for rule in wf:
            if rule[0] is None:
                continue
            cat, cmp, val = rule[0]
            nums[cat].append(val+0.5*((cmp == '>') - (cmp == '<')))
    for _, lst in nums.items():
        lst.append(0.5)
        lst.append(4000.5)
        lst.sort()
    pairs = {cat: [(a, b) for a, b in zip(lst, lst[1:])] for cat, lst in nums.items()}
    rtn = 0
    for comb in product(*pairs.values()):
        part = {cat: (a+b)/2 for cat, (a, b) in zip(cats, comb)}
        if accept(wfs, part):
            prod = 1
            for a, b in comb:
                prod *= int(b-a)
            rtn += prod
    return rtn


def send_ivl(wf, part):
    for rule in wf:
        if rule[0] is None:
            yield part.copy(), rule[1]
            continue
        cat, cmp, val = rule[0]
        a, b = part[cat]
        if cmp == '<':
            if val < a:
                pass
            if a < val < b:
                new = part.copy()
                new[cat] = (a, val-0.5)
                yield new, rule[1]
                part[cat] = (val-0.5, b)
            if b < val:
                yield part.copy(), rule[1]
        if cmp == '>':
            if val < a:
                yield part.copy(), rule[1]
            if a < val < b:
                new = part.copy()
                new[cat] = (val+0.5, b)
                yield new, rule[1]
                part[cat] = (a, val+0.5)
            if b < val:
                pass


def solve2_new(x):
    wfs, _ = x
    cats = list("xmas")
    stack = [({cat: (0.5, 4000.5) for cat in cats}, "in")]
    rtn = 0
    while stack:
        part, name = stack.pop()
        if name == "A":
            prod = 1
            for _, (a, b) in part.items():
                prod *= int(b-a)
            rtn += prod
            continue
        if name == "R":
            continue
        for new in send_ivl(wfs[name], part):
            stack.append(new)
    return rtn


solve2 = solve2_new


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
