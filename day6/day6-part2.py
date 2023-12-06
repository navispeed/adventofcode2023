import numba

with open("./input.txt") as fp:
    lines = fp.readlines()

race_time = int(lines[0].split(":")[1].replace(" ", ""))
max_distance = int(lines[1].split(":")[1].replace(" ", ""))


@numba.jit(fastmath=True, nopython=True, parallel=True)
def compute_total_distance(total_time, button_hold_time):
    current_speed = button_hold_time
    total_distance = 0
    for current_time in range(total_time - button_hold_time):
        total_distance += current_speed
    return total_distance


@numba.jit(fastmath=True, nopython=True, parallel=True)
def explore():
    total = 1

    win_count = 0
    for btn_hold in range(race_time):
        if compute_total_distance(race_time, btn_hold) > max_distance:
            win_count += 1
    total *= win_count
    print("*" * 50)

    print("res:", total)


if __name__ == '__main__':
    explore()
