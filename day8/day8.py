import math
from typing import Tuple

from sympy import primefactors

Edge = Tuple[str, str]

nodes_to_edge: dict[str, Edge] = {}
index_to_node: list[str] = []

with open("./input.txt") as fp:
    lines = fp.readlines()


def build_iterator():
    while True:
        for c in lines[0].strip():
            yield c


for line in lines[2:]:
    node, edges = tuple(line.split("="))
    nodes_to_edge[node.strip()] = edges.strip()[1:4], edges.strip()[6: 9]
    index_to_node.append(node.strip())

count = 0
min_count = 2 ** 32
start_nodes = list(filter(lambda n: n.endswith("Z"), index_to_node))

print(f"Found {len(start_nodes)} start nodes")

res = []
for current_node in start_nodes:
    for i, command in enumerate(build_iterator(), 1):
        current_node = nodes_to_edge[current_node][command == "R"]
        if current_node.endswith("Z"):
            res.append(i)
            break

print(res, math.lcm(*res))
for r in res:
    print(primefactors(r))
