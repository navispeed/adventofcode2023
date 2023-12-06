from typing import Tuple

import numba
from numba.typed import Dict


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


@numba.jit(fastmath=True, nopython=True)
def map_to_value(a_map: dict[int, Tuple[int, int]], point):
    r = 0
    for start, (destination, _range) in a_map.items():
        if start <= point <= start + _range:
            r = destination + (point - start)
    if r != 0:
        return r
    return point


@numba.jit(fastmath=True, nopython=True)
def seed_to_part2(entry_seeds: list[int],
                  seed_to_soil: dict[int, Tuple[int, int]]) -> list[int]:
    assert len(entry_seeds) % 2 == 0
    seeds: list[int] = [0]
    seeds.remove(0)  # hack for numba

    for start_pair_idx in range(0, len(entry_seeds), 2):
        start = entry_seeds[start_pair_idx]
        end = start + entry_seeds[start_pair_idx + 1]

        seeds.extend(range(start, end))

    return seeds


def to_numba_dict(original: dict):
    numba_dict = Dict()
    for k, v in original.items():
        if isinstance(v, dict):
            numba_dict[k] = to_numba_dict(v)
        else:
            numba_dict[k] = v
    return numba_dict


@numba.jit(fastmath=True, nopython=True, parallel=True)
def part2(maps, seeds: list[int]):
    seeds = seed_to_part2(seeds, maps["seed-to-soil"])
    min_location = 2 ** 32

    for seed_id in numba.prange(len(seeds)):
        seed = seeds[seed_id]
        current_location = seed
        current_location = map_to_value(maps["seed-to-soil"], current_location)
        current_location = map_to_value(maps["soil-to-fertilizer"], current_location)
        current_location = map_to_value(maps["fertilizer-to-water"], current_location)
        current_location = map_to_value(maps["water-to-light"], current_location)
        current_location = map_to_value(maps["light-to-temperature"], current_location)
        current_location = map_to_value(maps["temperature-to-humidity"], current_location)
        current_location = map_to_value(maps["humidity-to-location"], current_location)
        min_location = min(current_location, min_location)
    #
    print(min_location)


if __name__ == '__main__':
    with open("./input.txt") as fp:
        lines = list(fp.readlines())

    maps: dict[str, dict[int]] = parse(lines[2:])
    # seeds = seed_to_part2(extract_seed(lines[0]), numba_dict)
    part2(to_numba_dict(maps), extract_seed(lines[0]))

    # Part 1:
    # print(f"Seeds: {len(seeds)}")
    #
    # min_location = 2 ** 32
    #
    # for seed in list(seeds):
    #     current_location = seed
    #     current_location = map_to_value(maps["seed-to-soil"], current_location)
    #     current_location = map_to_value(maps["soil-to-fertilizer"], current_location)
    #     current_location = map_to_value(maps["fertilizer-to-water"], current_location)
    #     current_location = map_to_value(maps["water-to-light"], current_location)
    #     current_location = map_to_value(maps["light-to-temperature"], current_location)
    #     current_location = map_to_value(maps["temperature-to-humidity"], current_location)
    #     current_location = map_to_value(maps["humidity-to-location"], current_location)
    #
    #     print(seed, current_location)
    #     min_location = min(current_location, min_location)
    #
    # print(min_location)
