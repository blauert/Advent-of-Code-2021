# https://adventofcode.com/2021/day/17

import re

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    target = file.read()

target_re = re.compile('target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)')
t = target_re.search(target)
tx1, tx2, ty1, ty2 = int(t[1]), int(t[2]), int(t[3]), int(t[4])


def shoot(x_vel, y_vel):
    x = 0
    y = 0
    highest_point = 0
    while y > ty2 or x < tx1:
        x += x_vel
        y += y_vel
        if y > highest_point:
            highest_point = y
        if x_vel > 0:
            x_vel -= 1
        y_vel -= 1
    return x, y, highest_point


def check_hit(x, y):
    if x >= tx1 and x <= tx2 and y >= ty1 and y <= ty2:
        return True
    else:
        return False


# Part1 

# Find range of possible values for x velocity
x_vel_min = 0
x_shot = 0
while x_shot < tx1:
    x_vel_min += 1
    x_shot = ((x_vel_min**2)+x_vel_min)//2
x_vel_max = x_vel_min
while x_shot < tx2:
    x_vel_max += 1
    x_shot = ((x_vel_max**2)+x_vel_max)//2
# Find maximum possible y velocity
y_vel_max = abs(ty1)

# Try tickshots
highest_point = 0
for x_vel in range(x_vel_min, x_vel_max+1):
    for y_vel in range(0, y_vel_max):
        x, y, hp = shoot(x_vel, y_vel)
        if check_hit(x, y):
            if hp > highest_point:
                highest_point = hp

print(f"Highest point: {highest_point}")


# Part 2

num_velocities = 0
for x_vel in range(x_vel_min, tx2+1):
    for y_vel in range(ty1, y_vel_max):
        x, y, hp = shoot(x_vel, y_vel)
        if check_hit(x, y):
            num_velocities += 1

print(f"Distinct initial velocities: {num_velocities}")
