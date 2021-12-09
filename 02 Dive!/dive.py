# https://adventofcode.com/2021/day/2

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    commands = list([c.split() for c in file.readlines()])


# Part 1

horizontal_position = 0
depth = 0

for command in commands:
    direction = command[0]
    units = int(command[1])
    if direction == 'forward':
        horizontal_position += units
    if direction == 'down':
        depth += units
    if direction == 'up':
        depth -= units

print(horizontal_position * depth)


# Part 2

horizontal_position = 0
depth = 0
aim = 0

for command in commands:
    direction = command[0]
    units = int(command[1])

    if direction == 'forward':
        horizontal_position += units
        depth += (aim * units)
    if direction == 'down':
        aim += units
    if direction == 'up':
        aim -= units

print(horizontal_position * depth)
