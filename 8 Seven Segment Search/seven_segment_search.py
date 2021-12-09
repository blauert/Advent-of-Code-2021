# https://adventofcode.com/2021/day/8

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [[val.strip().split() for val in line.split(' | ')]
             for line in file.readlines()]

signal_patterns = {}
output_values = {}

for i, line in enumerate(lines):
    signal_patterns[i] = [set(pattern) for pattern in line[0]]
    output_values[i] = [set(value) for value in line[1]]


# Part 1

count = 0
for output in output_values.values():
    for v in output:
        if len(v) in {2, 3, 4, 7}:
            count += 1

print(f"Part 1: {count}")


# Part 2

result = 0
for display, patterns in signal_patterns.items():
    enc = {i: None for i in range(10)}  # encodings
    patterns_known = []
    patterns_5_letters = []
    patterns_6_letters = []

    for p in patterns:
        if len(p) == 6:
            patterns_6_letters.append(p)
        elif len(p) == 5:
            patterns_5_letters.append(p)
        else:
            patterns_known.append(p)

    for p in patterns_known:
        if len(p) == 2:                 # 1:   c  f
            enc[1] = p
        elif len(p) == 3:               # 7: a c  f
            enc[7] = p
        elif len(p) == 4:               # 4:  bcd f
            enc[4] = p
        elif len(p) == 7:               # 8: abcdefg
            enc[8] = p

    for p in patterns_5_letters:
        if p > enc[1]:                  # 3: a cd fg
            enc[3] = p
        elif p | enc[4] == enc[8]:      # 2: a cde g
            enc[2] = p
        else:                           # 5: ab d fg
            enc[5] = p

    for p in patterns_6_letters:
        if p > enc[4]:                  # 9: abcd fg
            enc[9] = p
        elif not p | enc[7] > enc[4]:   # 0: abc efg
            enc[0] = p
        else:                           # 6: ab defg
            enc[6] = p

    dec = {}  # decodings
    for num, encoding in enc.items():
        enc_str = ''
        for letter in encoding:
            enc_str += letter
        enc_str = ''.join(sorted(enc_str))
        dec[enc_str] = num

    number = 4 * [0]
    for k, v in enumerate(output_values[display]):
        val_str = ''
        for letter in v:
            val_str += letter
        val_str = ''.join(sorted(val_str))
        number[k] = dec[val_str]
    result += int(''.join([str(i) for i in number]))

print(f"Part 2: {result}")
