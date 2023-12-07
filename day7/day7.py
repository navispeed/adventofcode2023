import pattern

power = "AKQJT98765432"


def play(row: str):
    hand, bid = tuple(row.split())

    return pattern.handle_joker(hand), int(bid)


with open("./input.txt") as fp:
    lines = fp.readlines()
    r = sorted(list(map(play, lines)), key=lambda p: p[0], reverse=False)
    final_res_part1 = 0
    idx: int
    for idx, (hand, bid) in enumerate(list(r)):
        final_res_part1 += ((idx + 1) * bid)
    print(final_res_part1)
