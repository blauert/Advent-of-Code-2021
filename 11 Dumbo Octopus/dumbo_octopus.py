# https://adventofcode.com/2021/day/11

from collections import deque

input_file = 'real_input.txt'
#input_file = 'test_input_2.txt'
#input_file = 'test_input_1.txt'

with open(input_file) as file:
    grid = [[int(i) for i in line.strip()] for line in file.readlines()]


class Octopus:

    def __init__(self, value):
        self.value = value
        self.flashed = False

    def inc_value(self):
        self.value += 1
        if self.value > 9:
            self.flashed = True
            self.value = 0
        return self.flashed


class OctopusGrid:

    def __init__(self, grid):
        self.steps = 0
        self.flashes = 0
        self.curr_round_flashes = 0
        self.grid = {}
        """Coordinates:
        y: x->
        0: 0 1 2 3
        1: 0 1 2 3
        2: 0 1 2 3
        """
        x_max = len(grid[0])
        y_max = len(grid)
        for y in range(0, y_max):
            for x in range(0, x_max):
                self.grid[(x, y)] = Octopus(grid[y][x])

    def get_neighbors(self, coords):
        x = coords[0]
        y = coords[1]
        l = (x-1, y)
        r = (x+1, y)
        up = (x, y-1)
        up_l = (x-1, y-1)
        up_r = (x+1, y-1)
        down = (x, y+1)
        down_l = (x-1, y+1)
        down_r = (x+1, y+1)
        neighbors = []
        for coord in (l, r, up, down, up_l, up_r, down_l, down_r):
            neighbor = self.grid.get(coord)
            if neighbor is not None:
                neighbors.append((coord, neighbor))
        return neighbors

    def step(self):
        self.steps += 1
        self.curr_round_flashes = 0
        queue = deque()
        for coords, octopus in self.grid.items():
            octopus.flashed = False
            octopus.increased_neighbors = False
            queue.append((coords, octopus))

        while queue:
            coords, octopus = queue.popleft()
            flashed = False
            if not octopus.flashed:
                flashed = octopus.inc_value()
            if flashed:
                self.flashes += 1
                self.curr_round_flashes += 1
                neighbors = self.get_neighbors(coords)
                for n_coords, n_octopus in neighbors:
                    if not n_octopus.flashed:
                        queue.append((n_coords, n_octopus))


# Part 1

oct = OctopusGrid(grid)
for i in range(100):
    oct.step()
print(f"Octopus flashes: {oct.flashes}")


# Part 2

oct = OctopusGrid(grid)
while True:
    oct.step()
    if oct.curr_round_flashes == len(oct.grid):
        print(f"Flashes are synchronized after {oct.steps} steps.")
        break
