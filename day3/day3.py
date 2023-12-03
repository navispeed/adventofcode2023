import re
from typing import Tuple, Iterable, List


class Line:
    def __init__(self, line_as_str: str, symbols: list[str], numbers: list[int]):
        pass


Engine = list[Line]
Position = Tuple[int, int]


class Symbol:
    adjacent: list[int]

    def __init__(self, engine: Engine, position: Position):
        pass


def find_with_pos(pattern: str, line: str) -> Iterable[Tuple[Position, str]]:
    for match in re.finditer(pattern, line):
        yield match.start(), match.end(), match.group()


def explore_line(line: str):
    symbol_to_process = list(find_with_pos("([^\d^\.])", line))
    numbers = list(map(lambda tu: (tu[0], tu[1], int(tu[2])), find_with_pos("(\d+)", line)))
    # symbol_to_process = [] if symbol_to_process_res is None else symbol_to_process_res.groups()
    # numbers = [] if numbers_res is None else numbers_res.groups()
    return symbol_to_process, numbers


# def find_adjacent(prev_line)

Line = Tuple[list[Tuple[Position, str]], list[Tuple[Position, int]]]  # symbol, numbers


def explore(lines: list[str]):
    processed_lines = list(map(explore_line, lines))
    symbol_to_process: list[Tuple[Position, str]]
    numbers: list[Tuple[Position, int]]
    for idx, (symbol_to_process, _) in enumerate(processed_lines):
        print()


with open("./input.txt") as fp:
    lines = list(map(str.strip, fp.readlines()))

explore(lines)
