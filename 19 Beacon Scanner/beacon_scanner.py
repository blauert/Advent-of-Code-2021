# https://adventofcode.com/2021/day/19

from collections import defaultdict, deque
from itertools import combinations

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    input_lines = [line.strip().split(',') for line in file.readlines()]


class DeepSeaCoords:
    def get_distance(self, pair):
        x0, y0, z0 = pair[0][0], pair[0][1], pair[0][2]
        x1, y1, z1 = pair[1][0], pair[1][1], pair[1][2]
        if (x1 > x0) or ((x1 == x0) and (y1 > y0)) or ((x1 == x0) and (y1 == y0) and (z1 > z0)):
            hi, lo = pair[1], pair[0]
        else:
            hi, lo = pair[0], pair[1]
        return (lo, hi), (hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2])


class Map(DeepSeaCoords):
    def __init__(self, beacons):
        self.scanners = [(0, 0, 0)]
        self.beacons = set(beacons)
        self.distances = set()
        self.distances_to_coords = {}  # Good to know: distances between any two points are unique
        self.update_distances()

    def update_distances(self):
        for pair in combinations(self.beacons, 2):
            ordered_pair, distance = self.get_distance(pair)
            self.distances.add(distance)
            self.distances_to_coords[distance] = ordered_pair

    def add_scanner(self, scanner):
        success = False
        for or_id, distances in scanner.distances.items():
            overlap = self.distances & distances
            if len(overlap) >= 66:  # 12 beacons -> len([i for i in combinations(range(12), 2)]) == 66
                success = True
                break
        if not success:
            return False

        # Get current scanner offset
        dist = overlap.pop()  # Pick a point at random and match coordinates
        scanned_coords = scanner.distances_to_coords[or_id][dist]
        real_coords = self.distances_to_coords[dist]
        a = scanned_coords[0]
        b = real_coords[0]
        offset = (a[0]-b[0], a[1]-b[1], a[2]-b[2])

        # Add current scanner
        self.scanners.append(offset)
        # Update beacon coords
        updated_beacons = []
        for coords in scanner.orientations[or_id]:
            x, y, z = coords
            updated_coords = (x - offset[0], y - offset[1], z - offset[2])
            updated_beacons.append(updated_coords)
            self.beacons.add(updated_coords)
        # Update distances
        self.update_distances()
        return True


class Scanner(DeepSeaCoords):
    def __init__(self, beacons):
        # 24 possible orientations are numbered by id 0-23
        self.orientations = defaultdict(list)  # {id: [beacons], id: [beacons]}
        self.distances = {}  # {id: {distances}, id: {distances}}
        self.distances_to_coords = {}  # {id: {distance: pair}, id: {distance: pair}}

        for beacon in beacons:
            coords_rotated = self.rotate(beacon)
            for i in range(24):
                self.orientations[i].append(coords_rotated[i])

        for orientation_id, unknown_beacons in self.orientations.items():
            self.distances[orientation_id] = set()
            self.distances_to_coords[orientation_id] = {}
            for pair in combinations(unknown_beacons, 2):
                ordered_pair, distance = self.get_distance(pair)
                self.distances[orientation_id].add(distance)
                self.distances_to_coords[orientation_id][distance] = ordered_pair

    def rotate(self, coords):
        x, y, z = coords
        return [
            (x, y, z), (y, -x, z), (-x, -y, z), (-y, x, z),  # rotate around z axis
            (y, x, -z), (x, -y, -z), (-y, -x, -z), (-x, y, -z),  # -z axis
            (z, x, y), (x, -z, y), (-z, -x, y), (-x, z, y),  # y axis
            (x, z, -y), (z, -x, -y), (-x, -z, -y), (-z, x, -y),  # -y axis
            (y, z, x), (z, -y, x), (-y, -z, x), (-z, y, x),  # x axis
            (z, y, -x), (y, -z, -x), (-z, -y, -x), (-y, z, -x)  # -x axis
        ]


# Setup

scanner0_beacons = []
scanner0_done = False
unknown_beacons = []
for line in input_lines:
    if len(line) == 3:
        beacon = tuple(int(i) for i in line)
        if not scanner0_done:
            scanner0_beacons.append(beacon)
        else:
            unknown_beacons[-1].append(beacon)
    elif line == ['']:
        scanner0_done = True
        unknown_beacons.append([])

beacon_map = Map(scanner0_beacons)
scanners = deque()
for beacons in unknown_beacons:
    scanners.append(Scanner(beacons))

while scanners:
    scanner = scanners.popleft()
    if not beacon_map.add_scanner(scanner):
        scanners.append(scanner)


# Part 1

print(f"Number of beacons: {len(beacon_map.beacons)}")


# Part 2

def get_manhattan_distance(pair):
    x0, y0, z0 = pair[0][0], pair[0][1], pair[0][2]
    x1, y1, z1 = pair[1][0], pair[1][1], pair[1][2]
    return abs(x0-x1) + abs(y0-y1) + abs(z0-z1)


largest_man_dist = 0
for pair in combinations(beacon_map.scanners, 2):
    man_dist = get_manhattan_distance(pair)
    if man_dist > largest_man_dist:
        largest_man_dist = man_dist

print(f"Largest Manhattan distance: {largest_man_dist}")
