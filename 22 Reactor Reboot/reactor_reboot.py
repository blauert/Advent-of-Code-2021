# https://adventofcode.com/2021/day/22

from collections import Counter
import re

input_file = 'real_input.txt'
#input_file = 'test_input_2.txt'
#input_file = 'test_input_1.txt'
#input_file = 'test_input_0.txt'

with open(input_file) as file:
    lines = [line.strip() for line in file.readlines()]

command = re.compile(r'(on|off)\sx=(-?\d*)..(-?\d*),y=(-?\d*)..(-?\d*),z=(-?\d*)..(-?\d*)')

commands = []
for line in lines:
    mo = command.search(line)
    comm, x1, x2, y1, y2, z1, z2 = mo.groups()
    commands.append({'command': comm, 'x1': int(x1), 'x2': int(x2),
                     'y1': int(y1), 'y2': int(y2), 'z1': int(z1), 'z2': int(z2)})


# Part 1

cubes = {}
for c in commands:
    for x in range(max(-51, c['x1']), min(50, c['x2'])+1):
        for y in range(max(-51, c['y1']), min(50, c['y2'])+1):
            for z in range(max(-51, c['z1']), min(50, c['z2'])+1):
                if c['command'] == 'on':
                    cubes[(x, y, z)] = 'on'
                else:
                    cubes[(x, y, z)] = 'off'

print(f"Part 1: {Counter(cubes.values())['on']}")


# Part 2

class Cuboid:
    def __init__(self, x1=None, x2=None, y1=None, y2=None, z1=None, z2=None):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        if x1 is not None:
            self.cores = (self.x2+1 - self.x1) * (self.y2+1 - self.y1) * (self.z2+1 - self.z1)
        else:
            self.cores = 0

    def __repr__(self):
        return f"x={self.x1}..{self.x2},y={self.y1}..{self.y2},z={self.z1}..{self.z2},cores={self.cores}"

    def __bool__(self):
        if self.cores > 0:
            return True
        else:
            return False

    def __and__(self, other):
        if not self or not other:
            return Cuboid()
        new_x1 = max(self.x1, other.x1)
        new_x2 = min(self.x2, other.x2)
        new_y1 = max(self.y1, other.y1)
        new_y2 = min(self.y2, other.y2)
        new_z1 = max(self.z1, other.z1)
        new_z2 = min(self.z2, other.z2)
        if new_x2 >= new_x1 and new_y2 >= new_y1 and new_z2 >= new_z1:
            return Cuboid(new_x1, new_x2, new_y1, new_y2, new_z1, new_z2)
        else:
            return Cuboid()


def subtract_overlaps(cuboid, cuboids):
    count = cuboid.cores
    overlaps = []
    for other in cuboids:
        overlap = cuboid & other
        if overlap:
            overlaps.append(overlap)
    done = []
    for overlap in overlaps:
        count -= subtract_overlaps(overlap, done)
        done.append(overlap)
    return count


cuboids = []
for c in commands:
    cuboids.append([c['command'], Cuboid(c['x1'], c['x2'], c['y1'], c['y2'], c['z1'], c['z2'])])

count = 0
done = []
for curr in cuboids[::-1]:
    if curr[0] == 'on':
        count += subtract_overlaps(curr[1], done)
    done.append(curr[1])

print(f"Part 2: {count}")
