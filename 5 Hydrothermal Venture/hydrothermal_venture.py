# https://adventofcode.com/2021/day/5

from collections import Counter

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [[[int(i) for i in coords.split(',')]
              for coords in line.strip().split(' -> ')] for line in file.readlines()]

straight_lines = []
diagonal_lines = []
for line in lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    if x1 == x2 or y1 == y2:
        straight_lines.append(line)
    else:
        diagonal_lines.append(line)


# Part 1

points = []

for line in straight_lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    # Vertical line
    if x1 == x2:
        x = x1
        y_start = min(y1, y2)
        y_end = max(y1, y2)
        for y in range(y_start, y_end+1):
            points.append((x, y))
    # Horizontal line
    if y1 == y2:
        y = y1
        x_start = min(x1, x2)
        x_end = max(x1, x2)
        for x in range(x_start, x_end+1):
            points.append((x, y))

print(f"Part 1: {len([i for i in Counter(points).values() if i >= 2])}")


# Part 2

for line in diagonal_lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    x_start = min(x1, x2)
    x_end = max(x1, x2)
    y_start = min(y1, y2)
    y_end = max(y1, y2)
    # Main diagonal
    if (x1 > x2 and y1 > y2) or (x1 < x2 and y1 < y2):
        for coord in zip([x for x in range(x_start, x_end+1)], [y for y in range(y_start, y_end+1)]):
            points.append(coord)
    # Antidiagonal
    else:
        for coord in zip([x for x in range(x_start, x_end+1)], [y for y in range(y_end, y_start-1, -1)]):
            points.append(coord)

print(f"Part 2: {len([i for i in Counter(points).values() if i >= 2])}")
