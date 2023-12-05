import sys


def read_file(filename="input.txt"):
    with open(filename, "r") as f:
        return f.read().rstrip()


class Map:
    def __init__(self, rngs):
        self.rngs = tuple(rngs)

    def __getitem__(self, idx):
        match idx:
            case int():
                for dest, source, rng in self.rngs:
                    if idx in range(source, source + rng):
                        return dest + idx - source
                return idx
            case slice(start=start, stop=stop, step=None):
                rtn = []
                srcs = []
                for dest, source, rng in self.rngs:
                    if (itv_i := max(start, source)) < (itv_j := min(stop, source + rng)):
                        rtn.append(slice(itv_i+dest-source, itv_j+dest-source))
                        srcs.append(slice(itv_i, itv_j))
                srcs.sort()
                i = start
                j = None
                for slc in srcs:
                    j = slc.start
                    if slc.start > i:
                        rtn.append(slice(i, j))
                    i = slc.stop
                j = stop
                if j > i:
                    rtn.append(slice(i, j))
                return rtn


def parse(input_string):
    blocks = input_string.split("\n\n")
    seeds = [int(num) for num in blocks[0].split()[1:]]
    maps = [Map(tuple(int(num) for num in line.split()) for line in block.splitlines()[1:]) for block in blocks[1:]]
    return seeds, maps


def solve1(x):
    seeds, maps = x
    def process(seed, maps):
        val = seed
        for map in maps:
            val = map[val]
        return val
    return min(process(seed, maps) for seed in seeds)


def solve2(x):
    nums, maps = x
    seeds = [slice(nums[i], nums[i] + nums[i+1]) for i in range(0, len(nums), 2)]
    def process(seeds, maps):
        val = [seeds]
        for map in maps:
            val = [t for s in val for t in map[s]]
        return min(val).start
        # return val
    return min(process(seed, maps) for seed in seeds)
    # return min(sl for seed in seeds for sl in process(seed, maps)).start


if __name__ == "__main__":
    input_string = read_file(*sys.argv[1:])
    assert input_string.strip(), "File Empty"
    x = parse(input_string)
    res1 = solve1(x)
    print(f"Answer 1:\n{res1}\n")
    res2 = solve2(x)
    print(f"Answer 2:\n{res2}\n")
