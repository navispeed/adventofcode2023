import math
from collections import defaultdict

with open("./input.txt") as fp:
    lines = fp.readlines()

total = 0
scratch: dict[int, int] = defaultdict(lambda: 1)

for idx, line in enumerate(lines):
    s1_str, s2_str = tuple(line.split(":")[1].replace("\n", "").split(" | "))
    s1: list[int] = [int(i) for i in filter(len, s1_str.strip().split(" "))]
    s2: list[int] = [int(i) for i in filter(len, s2_str.strip().split(" "))]
    intersection = set(s1).intersection(s2)
    if len(intersection) > 0:
        total += (len(intersection) - 1) ** 2  # part 1
        for j in range(0, scratch[idx]):
            for i in range(idx + 1, idx + len(intersection) + 1):
                scratch[i] += 1
    else:
        scratch[idx] += 0  # if we never saw the card, force the card to exist. Else, do nothing.

print("part1", total, "part2:", sum(scratch.values()))
