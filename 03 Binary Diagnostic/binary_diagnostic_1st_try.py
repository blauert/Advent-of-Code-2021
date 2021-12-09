# https://adventofcode.com/2021/day/3

from collections import Counter

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    report = [line.strip() for line in file.readlines()]


# Part 1

gamma_rate = ''
for i in range(len(report[0])):
    count = Counter([num[i] for num in report])
    gamma_rate += count.most_common(1)[0][0]
gamma_decimal = int(gamma_rate, 2)

epsilon_rate = ''
for number in gamma_rate:
    complement = int(number) ^ 1  # XOR
    epsilon_rate += str(complement)
epsilon_decimal = int(epsilon_rate, 2)

print(f"Power Consumption = {gamma_decimal * epsilon_decimal}")


# Part 2

oxygen_gen = report.copy()
for i in range(len(report[0])):
    temp = []
    position_count = Counter([num[i] for num in oxygen_gen])
    if position_count['1'] >= position_count['0']:
        most_common = '1'
    else:
        most_common = '0'
    for num in oxygen_gen:
        if num[i] == most_common:
            temp.append(num)
    oxygen_gen = temp
    if len(oxygen_gen) == 1:
        oxygen_gen_rating = int(oxygen_gen[0], 2)
        break

co2_scrub = report.copy()
for i in range(len(report[0])):
    temp = []
    position_count = Counter([num[i] for num in co2_scrub])
    if position_count['0'] <= position_count['1']:
        least_common = '0'
    else:
        least_common = '1'
    for num in co2_scrub:
        if num[i] == least_common:
            temp.append(num)
    co2_scrub = temp
    if len(co2_scrub) == 1:
        co2_scrub_rating = int(co2_scrub[0], 2)
        break

print(f"Life Support Rating = {oxygen_gen_rating * co2_scrub_rating}")
