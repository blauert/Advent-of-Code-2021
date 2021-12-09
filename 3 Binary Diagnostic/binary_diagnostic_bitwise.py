# https://adventofcode.com/2021/day/3

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    report = [line.strip() for line in file.readlines()]

bit_length = len(report[0])
bit_report = [int(i, 2) for i in report]


# Part 1

gamma_rate = 0  # most common bit
epsilon_rate = 0  # least common bit

for i in range(bit_length):
    curr_bit = 1 << i
    counter = {0: 0, 1: 0}
    for num in bit_report:
        if num & curr_bit == curr_bit:
            counter[1] += 1
        else:
            counter[0] += 1
    if counter[1] > counter[0]:
        gamma_rate = gamma_rate | curr_bit
    else:
        epsilon_rate = epsilon_rate | curr_bit

print(f"Power Consumption = {gamma_rate * epsilon_rate}")


# Part 2

def bin_count(report, curr_bit):
    counter = {0: 0, 1: 0}
    for num in report:
        if num & curr_bit == curr_bit:
            counter[1] += 1
        else:
            counter[0] += 1
    return counter


oxygen_gen = bit_report.copy()
for i in range(bit_length-1, -1, -1):
    temp = []
    curr_bit = 1 << i
    counter = bin_count(oxygen_gen, curr_bit)
    if counter[1] >= counter[0]:
        most_common = 1
    else:
        most_common = 0
    for num in oxygen_gen:
        if (num & curr_bit) >> i == most_common:
            temp.append(num)
    oxygen_gen = temp
    if len(oxygen_gen) == 1:
        oxygen_gen_rating = oxygen_gen[0]
        break

co2_scrub = bit_report.copy()
for i in range(bit_length-1, -1, -1):
    temp = []
    curr_bit = 1 << i
    counter = bin_count(co2_scrub, curr_bit)
    if counter[0] <= counter[1]:
        least_common = 0
    else:
        least_common = 1
    for num in co2_scrub:
        if (num & curr_bit) >> i == least_common:
            temp.append(num)
    co2_scrub = temp
    if len(co2_scrub) == 1:
        co2_scrub_rating = co2_scrub[0]
        break

print(f"Life Support Rating = {oxygen_gen_rating * co2_scrub_rating}")
