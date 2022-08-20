import math
import string
import sys


class Constraints:
    sub_width: 3
    sub_height: 3
    size: 9
    row: list
    col: list
    block: list
    squares: list

    def __init__(self, big_size):
        self.sub_width = math.ceil(math.sqrt(big_size))
        self.sub_height = math.floor(math.sqrt(big_size))
        self.size = big_size
        self.row = list()
        self.col = list()
        self.block = list()
        self.squares = list()

        # Constraints
        for i in range(0, self.size):
            self.block.append(list())
        for i in range(0, self.size):
            r = list()
            c = list()
            for j in range(0, self.size):
                r.append(self.size * i + j)
                c.append(self.size * j + i)
                bX = i // self.sub_height
                bY = j // self.sub_width
                index = self.size * i + j
                block_num = bX * self.sub_height + bY
                self.block[block_num].append(index)
            self.row.append(r)
            self.col.append(c)

        # Individual Square constraints
        self.gen_constraints()

    def gen_constraints(self):
        for index in range(0, self.size * self.size):
            self.squares.append(set())
            for r in self.row:
                if index in r:
                    self.squares[index].update(r)
            for c in self.col:
                if index in c:
                    self.squares[index].update(c)
            for b in self.block:
                if index in b:
                    self.squares[index].update(b)

    def constrained_by(self, index):
        return self.squares[index]


charset = list()
charset.extend(string.digits)
charset.extend(string.ascii_uppercase)
charset.pop(0)
constraints = dict()


class Board:
    size: int
    con: Constraints
    state: str
    chars: list()

    def __init__(self, state):
        self.size = int(math.sqrt(len(state)))

        if self.size in constraints:
            self.con = constraints[self.size]
        else:
            self.con = Constraints(self.size)
            constraints[self.size] = self.con

        self.state = state
        self.chars = list()
        for i in range(0, self.size):
            self.chars.append(charset[i])

    def print(self):
        for i in range(0, self.size):
            for index in range(0, self.size):
                print(self.state[i * self.size + index], end=('  ' if index % 3 != 2 else ' | '))
            print('')
            if i % 3 == 2:
                print("-----------------------------")

    def num_each(self):
        res = dict()
        for char in self.state:
            if char in res:
                res[char] += 1
            else:
                res[char] = 1
        return res


def get_sorted_values(board, period):
    invalid: set = board.con.constrained_by(period)
    possibles: set = board.chars
    for tile in invalid:
        if board.state[tile] in possibles:
            possibles.remove(board.state[tile])
    return list(possibles)


def backtrack(board: Board):
    if '.' not in board.state:
        return board
    period = get_next(board)
    for attempt in get_sorted_values(board, period):
        new_state = board.state[:period] + attempt + board.state[period + 1:]
        child = Board(new_state)
        result = backtrack(child)
        if result is not None:
            return result
    return None


def get_next(board: Board):
    return board.state.index(".")


with open(sys.argv[1]) as f:
    for line in f:
        b = Board(line.split('\n')[0])
        print(backtrack(b).state)
