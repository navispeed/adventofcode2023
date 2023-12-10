import sys
from typing import List, Tuple, Iterable

import numpy

with open("./input.txt") as fp:
    lines: list[str] = list(map(lambda x: x.strip(), fp.readlines()))

Position = Tuple[int, int]
start_line = [i for i, line in enumerate(lines) if "S" in line][0]
start_index: Position = start_line, lines[start_line].find("S")
print(f"Start index is {start_index} ")
numpy.set_printoptions(threshold=sys.maxsize, linewidth=1000)
"""
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

"""

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""


def find_next(current: Position) -> list[Position]:
    """
    x is vertical (line)
    y is horizontal (column)
    :param current:
    :return:
    """
    case_to_check = set(
        [(current[0] - 1, y) for y in range(current[1] - 1, current[1] + 2) if
         y >= 0 and current[0] - 1 > 0] +
        [(current[0], y) for y in range(current[1] - 1, current[1] + 2) if
         y >= 0 and current[0] > 0] +
        [(current[0] + 1, y) for y in range(current[1] - 1, current[1] + 2) if
         y >= 0 and current[0] + 1 > 0]
    )

    # debug
    def validate(poss: Iterable[Position]) -> list[Position]:
        return list(
            filter(lambda pos: 0 <= pos[0] < len(lines) and 0 <= pos[1] < len(lines[0]) and
                               lines[pos[0]][pos[1]] != ".", poss))

    match lines[current[0]][current[1]]:
        case "S":
            return validate(case_to_check)
        case "|":
            return validate([(current[0] - 1, current[1]), (current[0] + 1, current[1])])
        case "-":
            return validate([(current[0], current[1] - 1), (current[0], current[1] + 1)])
        case "L":
            return validate([(current[0] - 1, current[1]), (current[0], current[1] + 1)])
        case "J":
            return validate([(current[0] - 1, current[1]), (current[0], current[1] - 1)])
        case "7":
            return validate([(current[0], current[1] - 1), (current[0] + 1, current[1])])  # S -> W
        case "F":
            return validate([(current[0] + 1, current[1]), (current[0], current[1] + 1)])  # S -> E
        case ".":
            return []
        case _:
            raise RuntimeError()


find_next(start_index)


def explore():
    seen: set[Position] = set()
    acc = [(start_index, 0, None)]
    while len(acc) > 0:
        current, c, prev = acc.pop(0)
        if current in seen:
            continue
        filled_map[current[0]][current[1]] = c
        seen.add(current)
        next_positions = find_next(current)
        if prev not in next_positions and prev is not None:
            continue
        for n in next_positions:
            if n in seen:
                continue
            acc.append((n, c + 1, current))
    for i in range(filled_map.max() - 1):
        if numpy.isclose(i, filled_map).sum() != 2:
            return False
    return True


# def debug(c: str):
#     match c:
#         case "S":
#             return "S"
#         case "|":
#             return "|"
#         case "-":
#             return "-"
#         case "L":
#             return validate([(current[0] - 1, current[1]), (current[0], current[1] + 1)])
#         case "J":
#             return validate([(current[0] - 1, current[1]), (current[0], current[1] - 1)])
#         case "7":
#             return validate([(current[0] - 1, current[1]), (current[0], current[1] + 1)])  # S -> W
#         case "F":
#             return validate([(current[0] + 1, current[1]), (current[0], current[1] + 1)])  # S -> E
#         case ".":
#             return []
#         case _:
#             raise RuntimeError()


for choice in "FJ|-7L":
    filled_map = numpy.array([[-1 for _ in range(len(lines[0]))] for i in range(len(lines))])
    l = lines[start_index[0]]
    l = l[:start_index[1]] + choice + l[start_index[1] + 1:]
    lines[start_index[0]] = l
    r = explore()
    print(filled_map)
    print("with", choice, "max:", filled_map.max(), numpy.isclose(filled_map, 1).sum(), r)

# class Pipe:
#     def __init__(self, current: Position, next: Position):
