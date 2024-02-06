import sys
from itertools import combinations
from math import lcm


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


def parse(input_string):
    lines = input_string.split("\n")
    dests = {}
    tps = {}
    for line in lines:
        key, val = line.split(" -> ")
        tp = ""
        if key[0] in ["%", "&"]:
            tp = key[0]
            key = key[1:]
        dests[key] = val.split(", ")
        tps[key] = tp
    return dests, tps


class Machine:
    def __init__(self, dests, tps):
        self.dests = {k: l.copy() for k, l in dests.items()}
        self.tps = tps.copy()
        add = {mod for lst in self.dests.values() for mod in lst}
        for new in add:
            if new not in self.dests:
                self.dests[new] = []
                self.tps[new] = ""
        self.inps = {}
        for key, lst in self.dests.items():
            self.inps.setdefault(key, [])
            for val in lst:
                self.inps.setdefault(val, []).append(key)
        self.states = {}
        for key, tp in self.tps.items():
            match tp:
                case "":
                    pass
                case "%":
                    self.states[key] = False
                case "&":
                    self.states[key] = {inp: False for inp in self.inps[key]}
        self.queue = []
        self.counts = [0, 0]
        self.rx = False

    def press(self, src="button", dest="broadcaster", hilo=False):
        self.send(src, dest, hilo)
        while self.queue:
            self.step()

    def inc(self, hilo):
        self.counts[hilo] += 1

    def send(self, src, dest, hilo):
        self.queue.append((src, dest, hilo))

    def step(self):
        src, dest, hilo = self.queue.pop(0)
        if not hilo and dest == "rx":
            self.rx = True
        # print(f"{src} -{'high' if hilo else 'low'}-> {dest}")
        self.inc(hilo)
        match self.tps[dest]:
            case "":
                for new in self.dests[dest]:
                    self.send(dest, new, hilo)
            case "%":
                if not hilo:
                    self.states[dest] = not self.states[dest]
                    for new in self.dests[dest]:
                        self.send(dest, new, self.states[dest])
            case "&":
                self.states[dest][src] = hilo
                val = not all(self.states[dest].values())
                for new in self.dests[dest]:
                    self.send(dest, new, val)

    def score(self):
        return self.counts[0] * self.counts[1]

    def num_states(self):
        rtn = 0
        for key, tp in self.tps.items():
            if tp == "%":
                rtn += 1
            elif tp == "&":
                rtn += len(self.states[key])
        return rtn

    def preds(self, key):
        seen = set()
        add = {key}
        while add:
            seen |= add
            add = {inp for k in add for inp in self.inps[k] if inp not in seen}
        return seen


def solve1(x, n=1000):
    mac = Machine(*x)
    for _ in range(n):
        mac.press()
    return mac.score()


def solve2(x):
    mac = Machine(*x)
    rx = "rx"
    assert not mac.dests[rx]
    assert len(mac.inps[rx]) == 1
    kl = mac.inps[rx][0]
    assert mac.tps[kl] == "&"
    ends = mac.inps[kl]
    for k1, k2 in combinations(ends, 2):
        assert mac.preds(k1) & mac.preds(k2) == {"broadcaster"}

    dests, tps = x
    macs = []
    for k in ends:
        preds = mac.preds(k)
        new_dests = {k: dests[k] for k in preds}
        new_tps = {k: tps[k] for k in preds}
        new_tps[kl] = "&"
        new_dests[kl] = [rx]
        macs.append(Machine(new_dests, new_tps))
    rtn = []
    for mac in macs:
        cnt = 0
        while not mac.rx:
            mac.press()
            cnt += 1
        rtn.append(cnt)
    return lcm(*rtn)


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
