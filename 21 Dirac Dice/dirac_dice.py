# https://adventofcode.com/2021/day/21

from collections import Counter, deque

p1, p2 = 10, 2  # real input
#p1, p2 = 4, 8  # test input


# Part 1

class DeterministicDie:
    def __init__(self):
        self.sides = deque(range(1, 100+1))

    def roll(self):
        val = self.sides.popleft()
        self.sides.append(val)
        return val


class Track:
    def __init__(self, start):
        self.position = start
        self.score = 0

    def move(self, rolled):
        new_pos = (self.position + rolled) % 10
        if new_pos == 0:
            new_pos = 10
        self.position = new_pos
        self.score += new_pos


die = DeterministicDie()
player1 = Track(p1)
player2 = Track(p2)
rolls = 0
turn = 1

while player1.score < 1000 and player2.score < 1000:
    rolled = die.roll() + die.roll() + die.roll()
    rolls += 3
    if turn == 1:
        player1.move(rolled)
        turn = 2
    elif turn == 2:
        player2.move(rolled)
        turn = 1

print(f"Part 1: {min(player1.score, player2.score) * rolls}")


# Part 2

# Rolling 3 times creates 27 universes, but only 7 different outcomes (3-9)
roll_weights = Counter()
for i in range(1, 3+1):
    for j in range(1, 3+1):
        for k in range(1, 3+1):
            roll_weights[i+j+k] += 1

# Instead of simulating every universe, group those w/ identical positions & scores
universes = {(p1, 0, p2, 0): 1}
player1_wins = 0
player2_wins = 0
turn = 1

while universes:
    uni_temp = Counter()
    for universe, count in universes.items():
        if turn == 1:
            player, score = universe[0], universe[1]
            p2, p2_score = universe[2], universe[3]
        elif turn == 2:
            p1, p1_score = universe[0], universe[1]
            player, score = universe[2], universe[3]
        player_wins = 0
        player_temp = Counter()

        # Simulate all 7 possible outcomes (3-9) and apply weights
        for i in range(3, 9+1):
            weight = roll_weights[i]
            curr_pos = player
            curr_score = score
            # Update player position and score
            new_pos = (curr_pos + i) % 10
            if new_pos == 0:
                new_pos = 10
            new_score = curr_score + new_pos
            # Check for win
            if new_score >= 21:
                player_wins += weight * count
            else:
                player_temp[(new_pos, new_score)] += weight * count

        # Save newly generated universes
        if turn == 1:
            player1_wins += player_wins
            for p, count in player_temp.items():
                uni_temp[(p[0], p[1], p2, p2_score)] += count
        elif turn == 2:
            player2_wins += player_wins
            for p, count in player_temp.items():
                uni_temp[(p1, p1_score, p[0], p[1])] += count

    # Setup for next round
    if turn == 1:
        turn = 2
    elif turn == 2:
        turn = 1
    universes = uni_temp

print(f"Part 2: {max(player1_wins, player2_wins)}")
