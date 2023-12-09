with open("./input.txt") as fp:
    lines = fp.readlines()


def extract(line: str) -> list[int]:
    return list(map(int, line.split()))


def dump(seqs: list[list[int]]):
    print("-" * 50)
    for idx, seq in enumerate(seqs):
        print("  " * idx + "   ".join(map(str, seq)))
    print("-" * 50)


def explore(line: list[int], past: bool) -> int:
    print("-" * 50)

    def diff(seq: list[int], acc: list[list[int]]):
        res = []
        for i in range(len(seq) - 1):
            res.append(seq[i + 1] - seq[i])
        acc.append(res)
        if all(map(lambda x: x == 0, res)):
            return acc
        return diff(res, acc)

    diff_res = diff(line, [line])
    r = sum(map(lambda arr: arr[-1], diff_res))

    print(diff_res, r)

    def reconstruct(seqs: list[list[int]]):
        dump(seqs)
        seqs[-1].insert(0, 0)
        for seq_id in reversed(range(len(seqs) - 2)):
            v = seqs[seq_id][0] - seqs[seq_id + 1][0]
            seqs[seq_id].insert(0, v)

        final_v = seqs[0][0]
        return final_v

    if past:  # part 2
        part2_res = reconstruct(diff_res)
        return part2_res
    return r


# print(sum(map(lambda x: explore(x, True), map(extract, lines))))  # Part 1
print(sum(map(lambda x: explore(x, True), map(extract, lines))))  # Part 1
