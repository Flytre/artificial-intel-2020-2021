import sys
from collections import deque

colors = ["R", "O", "Y", "G", "B", "P"]


class Board:
    size: int
    content: str
    connected: list
    parent = None
    length = 0

    def __init__(self, content, size, parent=None):
        self.content = content
        self.parent = parent
        self.size = int(size)

        if parent is None:
            self.length = 0
            self.connected = list()
            for i in range(0, len(self.content)):
                self.connected.append(False)
            self.connected[0] = True
        else:
            self.length = parent.length + 1
            self.connected = parent.connected.copy()

        if parent is None:
            temp = self.all_convertible_colors()

            while self.content[0] in temp:
                self.fix_connected(self.content[0])
                temp = self.all_convertible_colors()

    def isTouchingConnected(self, index):
        if self.connected[index]:
            return False
        if index % self.size > 0 and self.connected[index - 1]:
            return True
        if index % self.size < self.size - 1 and self.connected[index + 1]:
            return True
        if index >= self.size and self.connected[index - self.size]:
            return True
        if index < self.size ** 2 - self.size and self.connected[index + self.size]:
            return True
        return False

    def convertible(self):
        result = list()
        for i in range(0, self.size ** 2):
            if self.isTouchingConnected(i):
                result.append(i)
        return result

    def convertible_colors(self):
        current_color = self.content[0]
        tiles = self.convertible()
        result = list()
        for color in colors:
            if color not in self.content:
                continue
            if color == current_color:
                continue
            for tile in tiles:
                if self.content[tile] == color:
                    result.append(color)
                    break
        return result

    def all_convertible_colors(self):
        tiles = self.convertible()
        result = list()
        for color in colors:
            if color not in self.content:
                continue
            for tile in tiles:
                if self.content[tile] == color:
                    result.append(color)
                    break
        return result

    def make_children(self):
        result = list()
        for color in self.convertible_colors():
            result.append(self.convert(color))
        return result

    def convert(self, color):
        child = Board(self.content, self.size, self)
        tiles = self.convertible()

        for i in range(0, self.size ** 2):
            if self.connected[i]:
                child.content = child.content[:i] + color + child.content[i + 1:]

        for tile in tiles:
            if self.content[tile] == color:
                child.connected[tile] = True

        temp = child.all_convertible_colors()
        while child.content[0] in temp:
            child.fix_connected(child.content[0])
            temp = child.all_convertible_colors()

        return child

    def fix_connected(self, color):
        tiles = self.convertible()
        for tile in tiles:
            if self.content[tile] == color:
                self.connected[tile] = True

    def print_pretty(self):
        for i in range(0, self.size):
            line = ""
            for j in range(0, self.size):
                char = self.content[i * self.size + j]
                if not self.connected[i * self.size + j]:
                    char = char.lower()
                line += char
            print(line)
        print("")


def is_goal(board: Board):
    c = board.content[0]
    for i in range(0, board.size ** 2):
        if board.content[i] != c:
            return False
    return True


def solve(start: Board):
    to_visit = deque()
    visited: set = {start}
    to_visit.append(start)
    goal = None

    while len(to_visit) > 0:
        curr: Board = to_visit.popleft()
        if is_goal(curr):
            goal = curr
            break
        ch = curr.make_children()
        for chil in ch:
            if chil not in visited:
                to_visit.append(chil)
                visited.add(chil)

    return goal


with open(sys.argv[1]) as f:
    puzzle = ""
    size = 0
    for line in f:
        puzzle += line
        size = len(line)
    puzzle = "".join(puzzle.split())
    board = Board(puzzle, size, None)
    bo = solve(board)
    solution = list()
    l = 0
    while bo is not None:
        solution.append(bo)
        bo = bo.parent
        l += 1
    for i in range(len(solution) - 1, -1, -1):
        solution[i].print_pretty()
    print("length =", l)

