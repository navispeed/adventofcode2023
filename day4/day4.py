import math

with open("./input.txt") as fp:
    lines = fp.readlines()

total = 0

for line in lines:
    s1_str, s2_str = tuple(line.split(":")[1].replace("\n", "").split(" | "))
    s1: set[int] = {int(i) for i in filter(len, s1_str.strip().split(" "))}
    s2: set[int] = {int(i) for i in filter(len, s2_str.strip().split(" "))}
    intersection = s1.intersection(s2)
    print(s1, s2, intersection, math.pow(2, len(intersection) - 1))
    if len(intersection) > 0:
        total += math.pow(2, len(intersection) - 1)

print(total)
