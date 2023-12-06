with open("./input.txt") as fp:
    lines = fp.readlines()

times = list(map(int, lines[0].split(":")[1].split()))
distances = list(map(int, lines[1].split(":")[1].split()))

assert len(times) == len(distances)


# from functools import lru_cache
def compute_total_distance(total_time, button_hold_time):
    current_speed = 0
    total_distance = 0
    for current_time in range(total_time):
        if current_time < button_hold_time:
            current_speed += 1
        else:
            total_distance += current_speed
    return total_distance

total = 1

for i in range(len(times)):
    max_distance = distances[i]
    win_count = 0
    for race_time in range(times[i]):
        if is_win := compute_total_distance(times[i], race_time) > max_distance:
            print(f"With {race_time} ms on button, we win")
            win_count += 1
    total *= win_count
    print("*" * 50)

print("res:", total)


