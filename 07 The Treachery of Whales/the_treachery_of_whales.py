# https://adventofcode.com/2021/day/7

from statistics import mean, median

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    crab_positions = [int(i) for i in file.read().split(',')]


# Part 1

median_pos = int(median(crab_positions))

fuel_cost = 0
for pos in crab_positions:
    fuel_cost += abs(pos - median_pos)

print(f"Part 1: {fuel_cost}")


# Part 2

mean_pos = int(mean(crab_positions))

fuel_cost = 0
for pos in crab_positions:
    n = 1
    way = abs(pos - mean_pos)
    for i in range(way):
        fuel_cost += n
        n += 1

print(f"Part 2: {fuel_cost}")
