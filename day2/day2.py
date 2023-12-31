from collections import defaultdict

Subset = dict[str, int]
Game = list[Subset]


def process_subset(subset_line: str) -> Subset:
    res: Subset = {}
    for count_and_color_str in subset_line.split(","):  # [' 1 green', ' 3 red', ' 6 blue']
        count, color = (tuple(count_and_color_str.strip().split(" ")))
        res[color] = int(count)
    return res


def process_game(game_line: str) -> Game:
    """
    e.g [{'blue': 3, 'red': 4}, {'red': 1, 'green': 2, 'blue': 6}, {'green': 2}]
    :param game_line:
    :return:
    """
    return list(map(process_subset, game_line.split(";")))


def is_game_eligible(game: Game, params: Subset):  # Part 1
    def is_subset_ok(subset: Subset) -> bool:
        ok = True
        for color, count in subset.items():
            if params[color] < count:
                ok = False
        return ok

    return all(map(is_subset_ok, game))


def part2(game: Game) -> int:  # part 2, obviously
    def mul(*args: int):
        r = 1

        for arg in args:
            r *= arg

        return r

    res: Subset = defaultdict(lambda: 0)
    for subset in game:
        for color, count in subset.items():
            res[color] = max(res[color], count)
    return mul(*res.values())


with open("./input.txt") as fp:
    total = 0  # for part 1
    total_part_2 = 0
    for line in fp.readlines():
        game_id_str, game_info = tuple(line.split(":"))
        game_id = int(game_id_str.split(" ")[1])
        game = process_game(game_info)
        is_game_eligible_res = is_game_eligible(game, {"red": 12, "green": 13, "blue": 14})
        part_2_res = part2(game)
        print(game_id, game, "is eligible ? -> ",
              is_game_eligible_res, "fewest cube -> ", part_2_res)
        if is_game_eligible_res:
            total += game_id
        total_part_2 += part_2_res

print(total, total_part_2)
