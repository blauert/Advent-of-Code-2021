# https://adventofcode.com/2021/day/1

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    measurements = list(file.readlines())


# Part 1

increases = 0
for index, measurement in enumerate(measurements[1:]):
    if int(measurement) > int(measurements[index]):
        increases += 1

print(increases)


# Part 2

window_increases = 0
for i in range(len(measurements)-3):
    window_sum = int(measurements[i])\
        + int(measurements[i+1])\
        + int(measurements[i+2])
    next_window_sum = int(measurements[i+1])\
        + int(measurements[i+2])\
        + int(measurements[i+3])
    if next_window_sum > window_sum:
        window_increases += 1

print(window_increases)
