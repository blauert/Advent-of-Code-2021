# https://adventofcode.com/2021/day/9

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    grid = [[int(i) for i in line.strip()] for line in file.readlines()]


# Setup

"""Coordinates:
y: x->
0: 0 1 2 3
1: 0 1 2 3
2: 0 1 2 3
"""

x_max = len(grid[0])
y_max = len(grid)
points = {}

for y in range(0, y_max):
    for x in range(0, x_max):
        points[(x, y)] = grid[y][x]


# Solution

def get_neighbors(point):
    x = point[0]
    y = point[1]
    left = (x-1, y)
    right = (x+1, y)
    up = (x, y-1)
    down = (x, y+1)
    neighbors = {}
    for p in (left, right, up, down):
        val = points.get(p)  # None if coords out of range
        if val is not None:
            neighbors[p] = val
    return neighbors  # Dict of coords and values


def find_basin(point, basin):
    basin.add(point)
    neighbors = get_neighbors(point)
    for np, val in neighbors.items():
        if np not in basin:
            if val < 9:
                basin |= find_basin(np, basin)
    return basin


risk_levels = 0
basin_sizes = []

for y in range(0, y_max):
    for x in range(0, x_max):
        curr_point = (x, y)
        curr_val = points[curr_point]
        neighbors = get_neighbors(curr_point)

        # Find low points (Part 1)
        if curr_val < min(neighbors.values()):
            risk_levels += curr_val + 1

            # Find basins (Part 2)
            curr_basin = set()
            curr_basin |= find_basin(curr_point, curr_basin)
            basin_sizes.append(len(curr_basin))


print(f"Sum of all risk levels: {risk_levels}")  # Part 1

# Part 2
basin_sizes.sort()
print(f"Largest basins: {basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]}")
