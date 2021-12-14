# https://adventofcode.com/2021/day/13

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    dots = [line.strip() for line in file.readlines()]

instructions = []
while True:
    instr = dots.pop()
    if instr == '':
        break
    instructions.append(instr.strip('fold along ').split('='))
for instr in instructions:
    instr[1] = int(instr[1])

dots = [[int(i) for i in line.split(',')] for line in dots]

if instructions[-1][0] == 'x':
    grid_x = (instructions[-1][1] * 2) + 1
    grid_y = (instructions[-2][1] * 2) + 1
else:
    grid_y = (instructions[-1][1] * 2) + 1
    grid_x = (instructions[-2][1] * 2) + 1

grid = []
for y in range(grid_y):
    row = []
    for x in range(grid_x):
        row.append(0)
    grid.append(row)

for dot in dots:
    grid[dot[1]][dot[0]] = 1


def fold(instruction=None):
    if not instruction:
        instruction = instructions.pop()
    newgrid = []

    if instruction[0] == 'y':
        y_down = 0
        for y_up in range(len(grid)-1, instruction[1], -1):
            newline = []
            for i in range(len(grid[0])):
                newline.append(grid[y_up][i] | grid[y_down][i])
            y_down += 1
            newgrid.append(newline)

    if instruction[0] == 'x':
        for i in range(len(grid)):
            x_right = 0
            newline = []
            for x_left in range(len(grid[0])-1, instruction[1], -1):
                newline.append(grid[i][x_left] | grid[i][x_right])
                x_right += 1
            newgrid.append(newline)

    return newgrid


# Part 1

firstfold = fold(instruction=instructions[-1])

dots = 0
for row in firstfold:
    for num in row:
        if num == 1:
            dots += 1

print(f"Part 1: Dots after first fold: {dots}")


# Part 2

while instructions:
    grid = fold()

print("Part 2:")
for line in grid:
    for num in line:
        if num == 1:
            print('#', end='')
        else:
            print(' ', end='')
    print()
