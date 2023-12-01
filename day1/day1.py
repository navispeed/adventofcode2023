with open("./input.txt") as fp:
    total = 0
    for line in map(list, fp.readlines()):
        first_digit: str = next(filter(lambda c: ord(c) >= ord('0') and ord(c) <= ord('9'), line))
        last_digit: str = next(filter(lambda c: ord(c) >= ord('0') and ord(c) <= ord('9'), reversed(line)))
        number = int(first_digit+last_digit) # str
        total += number

print(total)
