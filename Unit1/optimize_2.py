from collections import deque
import time
import sys
import heapq


class Puzzle:
    board = ""
    parent = None
    size = 3
    length = 0
    goal_state = ""
    goal_dict = {}

    def __init__(self, board, size, parent=None):
        self.board = board
        self.parent = parent
        self.size = int(size)

        if parent is None:
            self.length = 0
        else:
            self.length = parent.length + 1

        sorted_array = (sorted(self.board))
        sorted_array.remove(".")
        sorted_array.append(".")
        self.goal_state = "".join(sorted_array)

        if parent is None:
            goal = self.goal_state
            for i, ch in enumerate(goal):
                self.goal_dict[ch] = i
        else:
            self.goal_dict = self.parent.goal_dict

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
        for index, char in enumerate(self.board):
            if self.goal_dict[char] != index:
                return False
        return True

    def goal_state(self):
        return self.goal_state

    def taxicab(self):
        score = 0
        for index, char in enumerate(self.board):
            if char == ".":
                continue
            loc = self.goal_dict[char]
            score += abs((self.board.index(char) % self.size) - (loc % self.size)) + abs(
                (self.board.index(char) // self.size) - (loc // self.size))

        for row in range(0, self.size):
            row_chars = list(self.board[i] for i in range(self.size * row, self.size * (row + 1)))
            filtered = [ch for ch in row_chars if ch != "." and self.belongs_in_row(ch)]
            current_streak = 0
            last_char = ""

            for index, ch in enumerate(filtered):
                if last_char == "":
                    current_streak = 1
                else:
                    if ch > last_char:
                        score += 2 * max(0, current_streak - 1)
                        current_streak = 1
                    else:
                        current_streak += 1
                last_char = ch
            score += 2 * max(0, current_streak - 1)

        for col in range(0, self.size):
            col_chars = list(self.board[i] for i in range(col, self.size ** 2, self.size))
            filtered = [ch for ch in col_chars if ch != "." and self.belongs_in_col(ch)]
            current_streak = 0
            last_char = ""

            for index, ch in enumerate(filtered):
                if last_char == "":
                    current_streak = 1
                else:
                    if ch > last_char:
                        score += 2 * max(0, current_streak - 1)
                        current_streak = 1
                    else:
                        current_streak += 1
                last_char = ch
            score += 2 * max(0, current_streak - 1)

        return score

    def belongs_in_row(self, char):
        """ Checks if a character is in the row it belongs in """
        goal_row = self.goal_dict[char] // self.size;
        row = self.board.find(char) // self.size
        return goal_row == row

    def belongs_in_col(self, char):
        """ Checks if a character is in the column it belongs in """
        goal_col = self.goal_dict[char] % self.size;
        col = self.board.find(char) % self.size
        return goal_col == col

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
    total_time = 0
    for line in f:

        if current_line > 31:
            quit(0)

        puzzle = Puzzle(line.split()[0], 4, None)
        can_solve, timer = timed(puzzle, solvable)
        if not can_solve:
            print("Line:", current_line, ", No solution found in", timer, "seconds.")

        else:
            astar, timer = timed(puzzle, a_star)
            print("Line:", current_line, ", A* - ", astar, "moves found in", timer, "seconds.")
        total_time += timer
        print()
        current_line += 1
    print("total time: ", total_time)
