import re
from typing import Tuple, Iterable

Position = Tuple[int, int]


def find_with_pos(pattern: str, line: str | None) -> Iterable[Tuple[int, int, str]]:
    if line is None:
        return
    for match in re.finditer(pattern, line):
        yield match.start(), match.end(), match.group()


def explore_line(line: str):
    symbol_to_process = list(find_with_pos("([^\d^\.])", line))
    numbers = list(map(lambda tu: (tu[0], tu[1], int(tu[2])), find_with_pos("(\d+)", line)))
    return symbol_to_process, numbers


Line = Tuple[list[Tuple[Position, str]], list[Tuple[Position, int]]]  # symbol, numbers


def explore_part2(lines: list[str]):
    processed_lines = list(map(explore_line, lines))
    idx: int
    total = 0
    for idx, (symbols, _) in enumerate(processed_lines):
        if len(symbols) == 0:
            continue
        for start, end, _ in symbols:
            total += check_symbol(end, idx, lines, start)
    print("Total", total)


def check_symbol(end, idx, lines, start):
    def compute_substr(line: str):
        _start: int = start
        _end: int = end
        for i in range(start - 1, -1, -1):
            if line[i].isnumeric():
                _start = i
                continue
            break
        for i in range(end, len(line)):
            if line[i].isnumeric():
                _end = i
                continue
            break
        if _start == -1 or _end == -1:
            return None
        return line[_start:_end + 1]

    numbers = []
    for line_index in range(max(0, idx - 1), min(len(lines), idx + 2)):
        substr = compute_substr(lines[line_index])
        m = list((find_with_pos(r"(\d+)", substr)))
        if len(m) == 1:
            numbers.append(int(m[0][2]))

    if len(numbers) == 2:
        return numbers[0] * numbers[1]
    return 0


def explore_part1(lines: list[str]):
    processed_lines = list(map(explore_line, lines))
    numbers: list[Tuple[Position, int]]
    idx: int
    total = 0
    for idx, (_, numbers) in enumerate(processed_lines):
        total += sum(check_numbers(idx, lines, numbers))
    print("Total", total)


def check_numbers(idx, lines, numbers):
    for start, end, number in numbers:
        number_ok = check_number(end, idx, lines, start)
        print(f"number_ok {number}", number_ok)
        if number_ok:
            yield number


def check_number(end, idx, lines, start):
    for line_index in range(max(0, idx - 1), min(len(lines), idx + 2)):
        substr = lines[line_index][max(0, start - 1): min(len(lines[line_index]), end + 1)]
        present = any((find_with_pos("([^\d^\.])", substr)))
        if present:
            return True
    return False


with open("./input.txt") as fp:
    lines = list(map(str.strip, fp.readlines()))

explore_part2(lines)
