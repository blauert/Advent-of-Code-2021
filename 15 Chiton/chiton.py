# https://adventofcode.com/2021/day/15

import heapq

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    map_data = [[int(i) for i in line.strip()] for line in file.readlines()]


def generate_grid(map_data):
    grid = {}
    for y in range(len(map_data)):
        for x in range(len(map_data[0])):
            grid[(x, y)] = map_data[y][x]
    return grid


def get_neighbors(coords):
    x = coords[0]
    y = coords[1]
    l = (x-1, y)
    r = (x+1, y)
    up = (x, y-1)
    down = (x, y+1)
    neighbors = {}
    for coord in (l, r, up, down):
        risk_level = grid.get(coord)
        if risk_level is not None:
            neighbors[coord] = risk_level
    return neighbors


def generate_graph(grid):
    graph = {}
    for field in grid:
        neighbor_risks = {}
        neighbors = get_neighbors(field)
        for coords, risk_level in neighbors.items():
            neighbor_risks[coords] = risk_level
        graph[field] = neighbor_risks
    return graph


def dijkstra(graph):
    start = (0, 0)
    costs = {field: float('inf') for field in graph}
    costs[start] = 0
    #parents = {}
    processed = set()
    min_dist = [(0, start)]

    while min_dist:

        cur_dist, cur = heapq.heappop(min_dist)
        if cur in processed:
            continue
        processed.add(cur)

        for neighbor in graph[cur]:
            if neighbor in processed:
                continue
            this_dist = cur_dist + graph[cur][neighbor]
            if this_dist < costs[neighbor]:
                costs[neighbor] = this_dist
                heapq.heappush(min_dist, (this_dist, neighbor))

    return costs


# Part 1

DATA = map_data
grid = generate_grid(DATA)
graph = generate_graph(grid)
costs = dijkstra(graph)
finish = (len(DATA[0])-1, len(DATA)-1)

print(f"Lowest total risk: {costs[finish]}")


# Part 2

map_x5 = []
for y in range(len(map_data)):
    new_row = []
    for i in range(5):
        for x in range(len(map_data[0])):
            new_val = (map_data[y][x] + i) % 9
            if new_val == 0:
                new_val = 9
            new_row.append(new_val)
    map_x5.append(new_row)

map_5x5 = []
for i in range(5):
    for y in range(len(map_x5)):
        new_row = []
        for x in range(len(map_x5[0])):
            new_val = (map_x5[y][x] + i) % 9
            if new_val == 0:
                new_val = 9
            new_row.append(new_val)
        map_5x5.append(new_row)

DATA = map_5x5
grid = generate_grid(DATA)
graph = generate_graph(grid)
costs = dijkstra(graph)
finish = (len(DATA[0])-1, len(DATA)-1)

print(f"Lowest total risk: {costs[finish]}")
