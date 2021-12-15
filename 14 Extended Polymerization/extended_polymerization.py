# https://adventofcode.com/2021/day/14

from collections import Counter

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [line.strip() for line in file.readlines()]

template = list(lines[0])
rules = {pair: elem for pair, elem in [
    rule.split(' -> ') for rule in lines[2:]]}


# Part 1

def polymerize(polymer):
    new_polymer = []
    for i in range(len(polymer)-1):
        new_polymer.append(polymer[i])
        pair = polymer[i] + polymer[i+1]
        new_polymer.append(rules[pair])
    new_polymer.append(polymer[-1])
    return new_polymer


polymer = template.copy()
for i in range(10):
    polymer = polymerize(polymer)
elements = Counter(polymer)
result = elements.most_common(1)[0][1] - elements.most_common()[-1][1]

print(f"Part 1: {result}")


# Part 2

# Last element (does not get modified)
last_elem = template[-1]

# Counter({'NN': 1, 'NC': 1, 'CB': 1})
polymer = Counter([template[i] + template[i+1] for i in range(len(template)-1)])

# {'CH': ['CB', 'BH'], 'HH': ['HN', 'NH'], 'CB': ['CH', 'HB'], ... }
rules2 = {pair: [pair[0]+elem, elem+pair[1]] for pair, elem in rules.items()}

# Polymerize
for i in range(40):
    temp = Counter()
    for pair, count in polymer.items():
        temp[rules2[pair][0]] += count
        temp[rules2[pair][1]] += count
    polymer = temp

# Count
elem_count = Counter(last_elem)  # account for last element
for pair, count in polymer.items():
    elem_count[pair[0]] += count

result = elem_count.most_common(1)[0][1] - elem_count.most_common()[-1][1]
print(f"Part 2: {result}")
