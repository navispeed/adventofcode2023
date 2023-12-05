from typing import Tuple


def build_map(buffer: list[str]) -> dict[int, Tuple[int, int]]:
    res = {}
    for line in buffer:
        if len(line) > 1:
            destination, start, _range = tuple(map(int, line.split()))
            res[start] = destination, _range

    return res


def parse(lines: list[str]) -> dict[str, dict[int]]:
    buffer: list[str] = []
    res = {}

    for line in lines:
        buffer.append(line)
        if len(line) == 1:
            name = buffer[0].split()[0]
            res[name] = build_map(buffer[1:])
            buffer = []

    name = buffer[0].split()[0]
    res[name] = build_map(buffer[1:])

    return res


def extract_seed(line: str) -> list[int]:
    return list(map(int, line.split(":")[1].split()))


def map_to_value(a_map: dict[int, Tuple[int, int]], point):
    for start, (destination, _range) in a_map.items():
        if start <= point <= start + _range:
            return destination + (point - start)
    return point


def seed_to_part2(entry_seeds: list[int]) -> list[int]:
    assert len(entry_seeds) % 2 == 0
    seeds = set()

    for start_pair_idx in range(0, len(entry_seeds), 2):
        start = entry_seeds[start_pair_idx]
        end = start + entry_seeds[start_pair_idx + 1]
        for s in range(start, end):
            seeds.add(s)

    return list(seeds)


if __name__ == '__main__':
    with open("./input-test.txt") as fp:
        lines = list(fp.readlines())

    seeds = seed_to_part2(extract_seed(lines[0]))

    maps = parse(lines[2:])

    min_location = 2 ** 32

    for seed in list(seeds):
        current_location = seed
        current_location = map_to_value(maps["seed-to-soil"], current_location)
        current_location = map_to_value(maps["soil-to-fertilizer"], current_location)
        current_location = map_to_value(maps["fertilizer-to-water"], current_location)
        current_location = map_to_value(maps["water-to-light"], current_location)
        current_location = map_to_value(maps["light-to-temperature"], current_location)
        current_location = map_to_value(maps["temperature-to-humidity"], current_location)
        current_location = map_to_value(maps["humidity-to-location"], current_location)

        print(seed, current_location)
        min_location = min(current_location, min_location)

    print(min_location)
