# https://adventofcode.com/2021/day/18

from copy import deepcopy
import itertools

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    numbers = [line.strip() for line in file.readlines()]


class NumberNode:
    def __init__(self, value, nesting_level):
        self.val = value
        self.lvl = nesting_level
        self.next = None
        self.prev = None


class SnailfishNumber:
    def __init__(self):
        self.head = NumberNode(None, 0)  # head sentinel
        self.tail = NumberNode(None, 0)  # tail sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def add(self, sfn):
        # This breaks the snailfish number being added
        prevnode = self.tail.prev
        nextnode = sfn.head.next
        prevnode.next = nextnode
        nextnode.prev = prevnode
        self.tail = sfn.tail
        # Update nesting levels
        node = self.head.next
        while node:
            node.lvl += 1
            node = node.next

    def reduce(self):
        explode_stack = []
        # Reverse through snailfish number and find all pairs to be exploded
        node = self.tail.prev
        while node:
            if node.lvl > 4:
                explode_stack.append(node.prev)
                node = node.prev.prev  # Only save the left node of a pair
            else:
                node = node.prev
        while True:
            # First finish all explodes
            if explode_stack:
                curr = explode_stack.pop()
                left_val = curr.val
                right_val = curr.next.val
                if curr.prev.val is not None:
                    curr.prev.val += left_val
                if curr.next.next.val is not None:
                    curr.next.next.val += right_val
                curr.val = 0
                curr.lvl -= 1
                curr.next = curr.next.next
                curr.next.prev = curr
            # Perform splits only after all explodes are done
            else:
                curr = None
                # Loop through snailfish number
                node = self.head.next
                while node.next is not None:
                    if node.val > 9:
                        curr = node
                        break
                    node = node.next
                if curr:
                    # Get new values & level
                    left_val = curr.val // 2
                    if curr.val % 2 == 0:
                        right_val = left_val
                    else:
                        right_val = curr.val // 2 + 1
                    level = curr.lvl + 1
                    # Set node attribues
                    curr.val = left_val
                    curr.lvl = level
                    right_node = NumberNode(right_val, level)
                    # Insert new right node
                    right_node.next = curr.next
                    right_node.prev = curr
                    curr.next = right_node
                    right_node.next.prev = right_node
                    # Add left node to explode stack if necessary
                    if level > 4:
                        explode_stack.append(curr)
                elif not curr:
                    break

    def get_magnitude(self):
        # This breaks the snailfish number
        for curr_lvl in range(4, 0, -1):
            node = self.head.next
            while node.next:
                if node.lvl == curr_lvl:
                    node.val = 3 * node.val + 2 * node.next.val
                    node.lvl = curr_lvl - 1
                    node.next = node.next.next
                node = node.next
        magnitude = self.head.next.val
        return magnitude


# Setup

snailfish_numbers = []
for num in numbers:
    sfn = SnailfishNumber()
    prevnode = sfn.head
    nesting_level = 0
    for char in num:
        if char == '[':
            nesting_level += 1
        elif char == ']':
            nesting_level -= 1
        elif char.isdigit():
            currnode = NumberNode(int(char), nesting_level)
            prevnode.next = currnode
            currnode.prev = prevnode
            sfn.tail.prev = currnode
            currnode.next = sfn.tail
            prevnode = currnode
    snailfish_numbers.append(sfn)


# Part 1

snailfish_num = deepcopy(snailfish_numbers[0])
for sfn in snailfish_numbers[1:]:
    sfn = deepcopy(sfn)
    snailfish_num.add(sfn)
    snailfish_num.reduce()

print(f"Magnitude: {snailfish_num.get_magnitude()}")


# Part 2

max_mag = 0
for perm in itertools.permutations(range(len(numbers)), 2):
    sfn1 = deepcopy(snailfish_numbers[perm[0]])
    sfn2 = deepcopy(snailfish_numbers[perm[1]])
    sfn1.add(sfn2)
    sfn1.reduce()
    magnitude = sfn1.get_magnitude()
    if magnitude > max_mag:
        max_mag = magnitude

print(f"Largest magnitude of any two snailfish numbers: {max_mag}")
