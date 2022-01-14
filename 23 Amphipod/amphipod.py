# https://adventofcode.com/2021/day/23

from collections import defaultdict
import heapq

input_file, input_file_2 = 'real_input.txt', 'real_input_part2.txt'
#input_file, input_file_2 = 'test_input.txt', 'test_input_part2.txt'

with open(input_file) as file:
    lines = [line.strip() for line in file.readlines()]
with open(input_file_2) as file:
    lines2 = [line.strip() for line in file.readlines()]


class Burrow:
    """
    # # # # # # # # # # # # #
    # 1 2   3   4   5   6 7 #  hallway
    # # # 2 # 2 # 2 # 2 # # #
        # 1 # 1 # 1 # 1 #      side rooms
        # # # # # # # # # 
          a   b   c   d
    """

    def __init__(self, amphipods):
        self.amphipods = amphipods
        self.done = self._check_done_()

    def __repr__(self):
        rooms = ('a1', 'a2', 'b1', 'b2', 'c1', 'c2', 'd1', 'd2')
        hallway = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7')
        b = {space: '.' for space in rooms + hallway}
        b.update(self.amphipods)
        return f'''{b['h1']}{b['h2']}{b['h3']}{b['h4']}{b['h5']}{b['h6']}{b['h7']}\
                   {b['a2']}{b['b2']}{b['c2']}{b['d2']}{b['a1']}{b['b1']}{b['c1']}{b['d1']}'''.replace(' ', '')

    def _check_done_(self):
        done = True
        if self.amphipods.get('a1') != 'A' or self.amphipods.get('a2') != 'A':
            done = False
        if self.amphipods.get('b1') != 'B' or self.amphipods.get('b2') != 'B':
            done = False
        if self.amphipods.get('c1') != 'C' or self.amphipods.get('c2') != 'C':
            done = False
        if self.amphipods.get('d1') != 'D' or self.amphipods.get('d2') != 'D':
            done = False
        return done

    def generate_graph(self):
        graph = defaultdict(dict)

        energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

        graph_out = {'a1': {'a2': 1}, 'a2': {'h2': 2, 'h3': 2},
                     'b1': {'b2': 1}, 'b2': {'h3': 2, 'h4': 2},
                     'c1': {'c2': 1}, 'c2': {'h4': 2, 'h5': 2},
                     'd1': {'d2': 1}, 'd2': {'h5': 2, 'h6': 2},
                     'h1': {}, 'h2': {'h1': 1},
                     'h3': {'h2': 2, 'h4': 2},
                     'h4': {'h3': 2, 'h5': 2},
                     'h5': {'h4': 2, 'h6': 2},
                     'h6': {'h7': 1}, 'h7': {}
                     }

        graph_in = {'h1': {'h2': 1},
                    'h2': {'h3': 2, 'a2': 2},
                    'h3': {'h4': 2, 'a2': 2, 'b2': 2},
                    'h4': {'h3': 2, 'h5': 2, 'b2': 2, 'c2': 2},
                    'h5': {'h4': 2, 'c2': 2, 'd2': 2},
                    'h6': {'h5': 2, 'd2': 2},
                    'h7': {'h6': 1},
                    'a2': {'a1': 1}, 'b2': {'b1': 1}, 'c2': {'c1': 1}, 'd2': {'d1': 1}
                    }

        rooms = {'a1', 'a2', 'b1', 'b2', 'c1', 'c2', 'd1', 'd2'}
        hallway = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'}

        for space, pod in self.amphipods.items():

            if space in rooms:
                room = space[0]
                tenant = room.upper()
                r1, r2 = f'{room}1', f'{room}2'
                if (space == r1 and pod == tenant) \
                        or ((space == r2 and pod == tenant) and self.amphipods.get(r1) == tenant):
                    continue
                visited = set(space)
                spaces = [(space, 0)]
                while spaces:
                    curr_s, curr_en = spaces.pop()
                    for next_s, next_en in graph_out[curr_s].items():
                        if next_s not in visited and self.amphipods.get(next_s) is None:
                            if next_s != r2:
                                graph[space][next_s] = (curr_en + next_en) * energy[pod]
                            spaces.append((next_s, curr_en+next_en))
                            visited.add(next_s)

            elif space in hallway:
                room = pod.lower()
                r1, r2 = f'{room}1', f'{room}2'
                other_rooms = {'a', 'b', 'c', 'd'} - {room}
                if self.amphipods.get(r1) is None and self.amphipods.get(r2) is None:
                    fin = r1
                elif self.amphipods.get(r1) == pod and self.amphipods.get(r2) is None:
                    fin = r2
                else:
                    continue
                visited = set(space)
                spaces = [(space, 0)]
                while spaces:
                    curr_s, curr_en = spaces.pop()
                    for next_s, next_en in graph_in[curr_s].items():
                        if next_s not in visited and next_s[0] not in other_rooms \
                                and self.amphipods.get(next_s) is None:
                            if next_s == fin:
                                graph[space][next_s] = (curr_en + next_en) * energy[pod]
                                spaces.clear()
                            else:
                                spaces.append((next_s, curr_en + next_en))
                                visited.add(next_s)
        return graph


class Burrow2:
    """
    # # # # # # # # # # # # #
    # 1 2   3   4   5   6 7 #  hallway
    # # # 4 # 4 # 4 # 4 # # #
        # 3 # 3 # 3 # 3 #
        # 2 # 2 # 2 # 2 #
        # 1 # 1 # 1 # 1 #      side rooms
        # # # # # # # # # 
          a   b   c   d
    """

    def __init__(self, amphipods):
        self.amphipods = amphipods
        self.done = self._check_done_()

    def __repr__(self):
        rooms = ('a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'd3', 'd4')
        hallway = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7')
        b = {space: '.' for space in rooms + hallway}
        b.update(self.amphipods)
        return f'''{b['h1']}{b['h2']}{b['h3']}{b['h4']}{b['h5']}{b['h6']}{b['h7']}\
                   {b['a4']}{b['b4']}{b['c4']}{b['d4']}\
                   {b['a3']}{b['b3']}{b['c3']}{b['d3']}\
                   {b['a2']}{b['b2']}{b['c2']}{b['d2']}\
                   {b['a1']}{b['b1']}{b['c1']}{b['d1']}'''.replace(' ', '')

    def _check_done_(self):
        done = True
        if self.amphipods.get('a1') != 'A' or self.amphipods.get('a2') != 'A' \
            or self.amphipods.get('a3') != 'A' or self.amphipods.get('a4') != 'A':
            done = False
        if self.amphipods.get('b1') != 'B' or self.amphipods.get('b2') != 'B' or \
            self.amphipods.get('b3') != 'B' or self.amphipods.get('b4') != 'B':
            done = False
        if self.amphipods.get('c1') != 'C' or self.amphipods.get('c2') != 'C' or \
            self.amphipods.get('c3') != 'C' or self.amphipods.get('c4') != 'C':
            done = False
        if self.amphipods.get('d1') != 'D' or self.amphipods.get('d2') != 'D' or \
            self.amphipods.get('d3') != 'D' or self.amphipods.get('d4') != 'D':
            done = False
        return done

    def generate_graph(self):
        graph = defaultdict(dict)

        energy = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

        graph_out = {'a1': {'a2': 1}, 'a2': {'a3': 1}, 'a3': {'a4': 1}, 'a4': {'h2': 2, 'h3': 2},
                     'b1': {'b2': 1}, 'b2': {'b3': 1}, 'b3': {'b4': 1}, 'b4': {'h3': 2, 'h4': 2},
                     'c1': {'c2': 1}, 'c2': {'c3': 1}, 'c3': {'c4': 1}, 'c4': {'h4': 2, 'h5': 2},
                     'd1': {'d2': 1}, 'd2': {'d3': 1}, 'd3': {'d4': 1}, 'd4': {'h5': 2, 'h6': 2},
                     'h1': {}, 'h2': {'h1': 1},
                     'h3': {'h2': 2, 'h4': 2},
                     'h4': {'h3': 2, 'h5': 2},
                     'h5': {'h4': 2, 'h6': 2},
                     'h6': {'h7': 1}, 'h7': {}
                     }

        graph_in = {'h1': {'h2': 1},
                    'h2': {'h3': 2, 'a4': 2},
                    'h3': {'h4': 2, 'a4': 2, 'b4': 2},
                    'h4': {'h3': 2, 'h5': 2, 'b4': 2, 'c4': 2},
                    'h5': {'h4': 2, 'c4': 2, 'd4': 2},
                    'h6': {'h5': 2, 'd4': 2},
                    'h7': {'h6': 1},
                    'a4': {'a3': 1}, 'a3': {'a2': 1}, 'a2': {'a1': 1},
                    'b4': {'b3': 1}, 'b3': {'b2': 1}, 'b2': {'b1': 1},
                    'c4': {'c3': 1}, 'c3': {'c2': 1}, 'c2': {'c1': 1},
                    'd4': {'d3': 1}, 'd3': {'d2': 1}, 'd2': {'d1': 1}
                    }

        rooms = {'a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'd3', 'd4'}
        hallway = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'}

        for space, pod in self.amphipods.items():

            if space in rooms:
                room = space[0]
                tenant = room.upper()
                r1, r2, r3, r4 = f'{room}1', f'{room}2', f'{room}3', f'{room}4'
                if pod == tenant:
                    if space == r1:
                        continue
                    elif self.amphipods.get(r1) == tenant:
                        if space == r2:
                            continue
                        elif self.amphipods.get(r2) == tenant:
                            if space == r3:
                                continue
                            elif self.amphipods.get(r3) == tenant:
                                if space == r4:
                                    continue

                visited = set(space)
                spaces = [(space, 0)]
                while spaces:
                    curr_s, curr_en = spaces.pop()
                    for next_s, next_en in graph_out[curr_s].items():
                        if next_s not in visited and self.amphipods.get(next_s) is None:
                            if next_s != r2 and next_s != r3 and next_s != r4:
                                graph[space][next_s] = (curr_en + next_en) * energy[pod]
                            spaces.append((next_s, curr_en+next_en))
                            visited.add(next_s)

            elif space in hallway:
                room = pod.lower()
                r1, r2, r3, r4 = f'{room}1', f'{room}2', f'{room}3', f'{room}4'
                other_rooms = {'a', 'b', 'c', 'd'} - {room}
                if self.amphipods.get(r1) is None and self.amphipods.get(r2) is None \
                    and self.amphipods.get(r3) is None and self.amphipods.get(r4) is None:
                    fin = r1
                elif self.amphipods.get(r1) == pod and self.amphipods.get(r2) is None \
                    and self.amphipods.get(r3) is None and self.amphipods.get(r4) is None:
                    fin = r2
                elif self.amphipods.get(r1) == pod and self.amphipods.get(r2) == pod \
                    and self.amphipods.get(r3) is None and self.amphipods.get(r4) is None:
                    fin = r3
                elif self.amphipods.get(r1) == pod and self.amphipods.get(r2) == pod \
                    and self.amphipods.get(r3) == pod and self.amphipods.get(r4) is None:
                    fin = r4
                else:
                    continue
                visited = set(space)
                spaces = [(space, 0)]
                while spaces:
                    curr_s, curr_en = spaces.pop()
                    for next_s, next_en in graph_in[curr_s].items():
                        if next_s not in visited and next_s[0] not in other_rooms \
                                and self.amphipods.get(next_s) is None:
                            if next_s == fin:
                                graph[space][next_s] = (curr_en + next_en) * energy[pod]
                                spaces.clear()
                            else:
                                spaces.append((next_s, curr_en + next_en))
                                visited.add(next_s)
        return graph


def find_least_energy(burrow, part=1):
    # https://docs.python.org/3/library/heapq.html?highlight=tie-breaker#priority-queue-implementation-notes
    tie_breaker = 0
    min_burrows = [(0, tie_breaker, burrow)]
    least_energy = float('inf')
    processed = set()
    if part == 1:
        Burr = Burrow
    elif part == 2:
        Burr = Burrow2
    while min_burrows:
        curr_energy, br, curr = heapq.heappop(min_burrows)
        configuration = str(curr)
        if configuration in processed:
            continue
        processed.add(configuration)
        graph = curr.generate_graph()
        for old_space, moves in graph.items():
            for new_space, energy in moves.items():
                new_energy = curr_energy + energy
                if new_energy < least_energy:
                    new_amphipods = curr.amphipods.copy()
                    new_amphipods[new_space] = new_amphipods.pop(old_space)
                    new_burrow = Burr(new_amphipods)
                    if new_burrow.done == True:
                        least_energy = new_energy
                    else:
                        configuration = str(new_burrow)
                        if configuration in processed:
                            continue
                        tie_breaker += 1
                        heapq.heappush(min_burrows, (new_energy, tie_breaker, new_burrow))
    return least_energy


# Part 1

b = Burrow({'a1': lines[3][1], 'a2': lines[2][3],
            'b1': lines[3][3], 'b2': lines[2][5],
            'c1': lines[3][5], 'c2': lines[2][7],
            'd1': lines[3][7], 'd2': lines[2][9]})

print(f"Part 1: {find_least_energy(b)}")


# Part 2

b = Burrow2({'a1': lines2[5][1], 'a2': lines2[4][1], 'a3': lines2[3][1], 'a4': lines2[2][3],
             'b1': lines2[5][3], 'b2': lines2[4][3], 'b3': lines2[3][3], 'b4': lines2[2][5],
             'c1': lines2[5][5], 'c2': lines2[4][5], 'c3': lines2[3][5], 'c4': lines2[2][7],
             'd1': lines2[5][7], 'd2': lines2[4][7], 'd3': lines2[3][7], 'd4': lines2[2][9]})

print(f"Part 2: {find_least_energy(b, 2)}")
