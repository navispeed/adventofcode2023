MAPPING = {
    0: "zero",
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

TOKEN = set(MAPPING.keys()).union(REVERSED_MAPPING.keys())

with open("./input.txt") as fp:
    total = 0
    for line in fp.readlines():
        pos = {token: p for token in TOKEN if ((p := line.find(str(token))) != -1)}
        first_digit: str = str(REVERSED_MAPPING[min(pos.items(), key=lambda p: p[1])[0]])
        last_digit: str = str(REVERSED_MAPPING[max(pos.items(), key=lambda p: p[1])[0]])
        number = int(first_digit + last_digit)  # str
        total += number

print(total)
