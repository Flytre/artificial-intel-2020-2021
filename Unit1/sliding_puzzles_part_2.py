from collections import deque
import time
import sys
import heapq


class Puzzle:
    board = ""
    parent = None
    size = 3
    length = 0

    def __init__(self, board, size, parent=None):
        self.board = board
        self.parent = parent
        self.size = int(size)

        if parent is None:
            self.length = 0
        else:
            self.length = parent.length + 1

    def __eq__(self, obj):
        return isinstance(obj, Puzzle) and obj.board == self.board

    def __hash__(self):
        return hash(self.board)

    def get_parent(self):
        return self.parent

    def get_size(self):
        return self.size

    def get_board(self):
        return self.board

    def __str__(self):
        returned = ""
        for i in range(0, self.size):
            returned += " ".join(list(self.board[(i * self.size):(i * self.size) + self.size]))
            if i < self.size - 1:
                returned += "\n"
        return returned

    def __gt__(self, other):
        if self.board > other.board:
            return True
        else:
            return False

    def get_blank(self):
        return self.board.index(".")

    def get_length(self):
        return self.length

    def is_goal(self):
        if self.board[-1] != ".":
            return False

        last = self.board[0]
        for char in self.board:
            if char == ".":
                continue
            if char < last:
                return False
            last = char
        return True

    def goal_state(self):
        sorted_array = (sorted(self.board))
        sorted_array.remove(".")
        sorted_array.append(".")
        return Puzzle("".join(sorted_array), self.size, self.parent)

    def taxicab(self):
        goal = self.goal_state().get_board()
        score = 0
        for index, char in enumerate(self.board):
            if char == ".":
                continue
            loc = goal.index(char)
            score += abs((self.board.index(char) % self.size) - (loc % self.size)) + abs(
                (self.board.index(char) // self.size) - (loc // self.size))

        return score

    def swap(self, i, j):
        ls = list(self.board)
        ls[i], ls[j] = ls[j], ls[i]
        return Puzzle("".join(ls), self.size, self)

    def make_children(self):
        blank = self.get_blank()
        blank_row, blank_col = blank // self.size, blank % self.size
        swaps = []

        if blank_row > 0:
            swaps.append(self.swap(blank, blank - self.size))
        if blank_row < self.size - 1:
            swaps.append(self.swap(blank, blank + self.size))
        if blank_col > 0:
            swaps.append(self.swap(blank, blank - 1))
        if blank_col < self.size - 1:
            swaps.append(self.swap(blank, blank + 1))

        return swaps

    def parity(self):
        parity = 0
        visited: list = []
        for char in self.get_board():
            parity += len([i for i in visited if char != "." and i != "." and char < i])
            visited.append(char)
        return parity


def timed(initial, method):
    start = time.perf_counter()
    ret = method(initial)
    end = time.perf_counter()
    t = (end - start)
    return ret, t


def solvable(puzzle):
    if puzzle.get_size() % 2 == 1:
        return puzzle.parity() % 2 == 0
    return (puzzle.get_blank() // puzzle.get_size()) % 2 != (puzzle.parity() % 2)


def a_star(puzzle: Puzzle):
    closed = set()
    start_val = (puzzle.get_length() + puzzle.taxicab(), puzzle)
    fringe = [start_val]
    heapq.heapify(fringe)

    while len(fringe) > 0:
        item = heapq.heappop(fringe)
        if item[1].is_goal():
            return item[1].get_length()
        if item[1] not in closed:
            closed.add(item[1])
            children = item[1].make_children()
            for child in children:
                if child not in closed:
                    heapq.heappush(fringe, (child.get_length() + child.taxicab(), child))
    return None


with open("15_puzzles.txt") as f:
    current_line = 0
    for line in f:
        puzzle = Puzzle(line.split()[0], 4, None)
        can_solve, timer = timed(puzzle, solvable)
        if not can_solve:
            print("Line:", current_line, ", No solution found in", timer, "seconds.")

        else:
                astar, timer = timed(puzzle, a_star)
                print("Line:", current_line, ", A* - ", astar, "moves found in", timer, "seconds.")
        print()
        current_line += 1
