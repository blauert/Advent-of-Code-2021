# https://adventofcode.com/2021/day/10

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [line.strip() for line in file.readlines()]

chars = {'(': ')', '[': ']', '{': '}', '<': '>'}

illegal_chars = []  # Part 1
missing_closing_chars = []  # Part 2

for line in lines:
    stack = []
    for char in line:
        if char in chars:
            stack.append(chars[char])
        else:
            # Corrupted line
            expected = stack.pop()
            if char != expected:
                illegal_chars.append(char)
                stack = None
                break
    if stack:
        # Incomplete line
        expected = stack[::-1]
        missing_closing_chars.append(expected)


# Part 1

illegal_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
error_score = 0
for char in illegal_chars:
    error_score += illegal_scores[char]

print(f"Part 1: Syntax error score: {error_score}")


# Part 2

completion_scores = {')': 1, ']': 2, '}': 3, '>': 4}
scores = []
for line in missing_closing_chars:
    line_score = 0
    for char in line:
        line_score *= 5
        line_score += completion_scores[char]
    scores.append(line_score)

scores.sort()
print(f"Part 2: Middle score: {scores[len(scores) // 2]}")
