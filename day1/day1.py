import time

MAPPING = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine"
}

REVERSED_MAPPING = {v: k for k, v in MAPPING.items()}
REVERSED_MAPPING.update({k: k for k, v in MAPPING.items()})

TOKEN = set(MAPPING).union(REVERSED_MAPPING)


def process_line(line):
    pos = {token: p for token in TOKEN if (p := line.find(str(token))) != -1}
    rpos = {token: p for token in TOKEN if (p := line.rfind(str(token))) != -1}

    first_digit: str = str(REVERSED_MAPPING[min(pos, key=pos.get)])
    last_digit: str = str(REVERSED_MAPPING[max(rpos, key=rpos.get)])
    return int(first_digit + last_digit)


t0 = time.time()
with open("./input.txt") as fp:
    lines = fp.readlines()

total = sum(process_line(line) for line in lines)
print(total, f"in {time.time() - t0} seconds for regular")
