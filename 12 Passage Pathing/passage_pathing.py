# https://adventofcode.com/2021/day/12

from collections import defaultdict, deque

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [line.strip().split('-') for line in file.readlines()]

start = 'start'
end = 'end'

graph = defaultdict(list)
for parent, child in lines:
    if not child == start:
        graph[parent].append(child)
    if not parent == start:
        graph[child].append(parent)


# Part 1

paths = deque([{'node': start, 'visited': set()}])
paths_done = 0

while paths:
    p = paths.popleft()
    lastnode = p['node']
    vis = p['visited']
    children = graph[lastnode]
    for child in children:
        if child == end:  # end
            paths_done += 1
        elif child.upper() == child:  # uppercase
            paths.append({'node': child, 'visited': vis})
        else:  # lowercase
            if child not in vis:
                paths.append({'node': child, 'visited': vis | set([child])})

print(f"Part 1: Paths through the cave system: {paths_done}")


# Part 2

paths = deque([{'node': start, 'visited': set(), 'vis_twice': False}])
paths_done = 0

while paths:
    p = paths.popleft()
    lastnode = p['node']
    vis = p['visited']
    vis2 = p['vis_twice']
    children = graph[lastnode]
    for child in children:
        if child == end:  # end
            paths_done += 1
        elif child.upper() == child:  # uppercase
            paths.append({'node': child, 'visited': vis, 'vis_twice': vis2})
        else:  # lowercase
            if child not in vis:
                paths.append({'node': child, 'visited': vis | set([child]), 'vis_twice': vis2})
            elif vis2 == False:
                paths.append({'node': child, 'visited': vis | set([child]), 'vis_twice': True})

print(f"Part 2: Paths through the cave system: {paths_done}")
