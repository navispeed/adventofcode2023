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
    eligible_numbers: set[Tuple[int, int]]
    idx: int
    total = 0
    for idx, (_, numbers) in enumerate(processed_lines):
        total += sum(check_numbers(idx, lines, numbers))
    print("Total", total)


def check_numbers(idx, lines, numbers):
    for start, end, number in numbers:
        number_ok = False
        number_ok = check_number(end, idx, lines, number_ok, start)
        print(f"number_ok {number}", number_ok)
        if number_ok:
            yield number


def check_number(end, idx, lines, number_ok, start):
    for line_index in range(max(0, idx - 1), min(len(lines), idx + 2)):
        substr = lines[line_index][max(0, start - 1): min(len(lines[line_index]), end + 1)]
        present = any((find_with_pos("([^\d^\.])", substr)))
        if present:
            return True
    return False


with open("./input.txt") as fp:
    lines = list(map(str.strip, fp.readlines()))

explore(lines)
