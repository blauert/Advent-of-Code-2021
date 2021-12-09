# https://adventofcode.com/2021/day/4

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    bingo = [line.strip() for line in file.readlines() if line.strip()]

bingo_numbers = [int(i) for i in bingo[0].split(',')]

bingo_boards = []
for i in range(0, len(bingo[1:]), 5):
    bingo_boards.append([])
    for j in range(5):
        bingo_boards[-1].append([int(i) for i in bingo[1:][i+j].split()])


class Board:
    """Coordinates:
    y: x->
    0: 0 1 2 3 4
    1: 0 1 2 3 4
    2: 0 1 2 3 4
    3: 0 1 2 3 4
    4: 0 1 2 3 4
    """

    def __init__(self):
        self.nums_coords = {}  # {23:(0,0),50:(3,4),17:(2,1), etc... }
        self.x_counter = {}  # {0:0,1:0,2:0,3:0,4:0}
        self.y_counter = {}  # {0:0,1:0,2:0,3:0,4:0}

    def setup(self, board):
        for y in range(len(board)):
            self.x_counter[y] = 0
            self.y_counter[y] = 0
            row = board[y]
            for x in range(len(row)):
                num = row[x]
                self.nums_coords[num] = (x, y)

    def check(self, number):
        if number in self.nums_coords:
            coords = self.nums_coords.pop(number)
            x = coords[0]
            y = coords[1]
            self.x_counter[x] += 1
            self.y_counter[y] += 1
            if self.x_counter[x] == 5 or self.y_counter[y] == 5:  # Bingo
                unmarked = sum(self.nums_coords)
                score = unmarked * number
                return score
        else:
            return 0


class Bingo:

    def __init__(self):
        self.playing_boards = []
        self.winner = False

    def draw(self, number):
        winners = []
        for board in self.playing_boards:
            score = board.check(number)
            if score:
                winners.append(board)
                if not self.winner:
                    self.winner = True
                    print(f"Bingo! First winner: {score}")
        for board in winners:
            self.playing_boards.remove(board)
        if winners and not self.playing_boards:
            print(f"Bingo ¯\_(ツ)_/¯ Last winner: {score}")

    def addBoard(self, board):
        new_board = Board()
        new_board.setup(board)
        self.playing_boards.append(new_board)


squid_game = Bingo()

for board in bingo_boards:
    squid_game.addBoard(board)

for number in bingo_numbers:
    squid_game.draw(number)
