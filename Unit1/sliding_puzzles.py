from collections import deque
import time
import sys


class Puzzle:
    content = ""
    parent = None
    size = 3
    length = 0

    def __init__(self, content, size, parent=None, length=0):
        self.content = content
        self.parent = parent
        self.size = int(size)
        self.length = length

    def __eq__(self, obj):
        return isinstance(obj, Puzzle) and obj.content == self.content

    def __hash__(self):
        return hash(self.content)

    def get_parent(self):
        return self.parent

    def get_content(self):
        return self.content

    def __str__(self):
        returned = ""
        for i in range(0, self.size):
            returned += " ".join(list(self.content[(i * self.size):(i * self.size) + self.size]))
            if i < self.size - 1:
                returned += "\n"
        return returned

    def get_blank(self):
        return self.content.index(".")

    def get_length(self):
        return self.length

    def is_goal(self):
        if self.content[-1] != ".":
            return False

        last = self.content[0]
        for char in self.content:
            if char == ".":
                continue
            if char < last:
                return False
            last = char
        return True

    def goal_state(self):
        sorted_array = (sorted(self.content))
        sorted_array.remove(".")
        sorted_array.append(".")
        return Puzzle("".join(sorted_array), self.size, self.parent)

    def swap(self, i, j):
        ls = list(self.content)
        ls[i], ls[j] = ls[j], ls[i]
        return Puzzle("".join(ls), self.size, self, self.length + 1)

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


def modeling_task_1():
    with open("slide_puzzle_tests.txt") as f:
        current_line = 0
        for line in f:
            puzzle = Puzzle(line.split()[1], line.split()[0], None)
            print("Line", current_line, "start state:")
            print(puzzle)
            print("Line", current_line, "children:")
            for child in puzzle.make_children():
                print(child)
                print()
            print("Line", current_line, "goal state:")
            print(puzzle.goal_state())
            print()
            current_line += 1


def solve(start):
    to_visit = deque()
    visited: set = {start}
    to_visit.append(start)
    goal = None

    while len(to_visit) > 0:
        curr = to_visit.popleft()
        if curr.is_goal():
            goal = curr
            break
        children = curr.make_children()
        for child in children:
            if child not in visited:
                to_visit.append(child)
                visited.add(child)

    return goal.get_length()


def time_solve(initial):
    start = time.perf_counter()
    len = solve(initial)
    end = time.perf_counter()
    t = (end - start)
    return len, t


def longest_8_puzzle():
    shortest = Puzzle("12345678.", 3)
    visited: set = {shortest}
    to_visit = deque()
    to_visit.append(shortest)

    while len(to_visit) > 0:
        curr = to_visit.popleft()
        children = curr.make_children()
        for child in children:
            if child not in visited:
                to_visit.append(child)
                visited.add(child)
    max = 0
    for combo in visited:
        if combo.get_length() > max:
            max = combo.get_length()

    print("Max Solution Length:", max)
    print("Puzzles with Maximum Solution Length:")
    for combo in visited:
        if combo.get_length() == max:
            print("Puzzle:")
            print(combo, end="\n\n")
            print("Path to Solution:")
            pather = combo
            while pather.get_parent() is not None:
                print(pather, end="\n\n")
                pather = pather.get_parent()
            print(pather, end="\n\n\n")


args: list = sys.argv

with open(args[1]) as f:
    current_line = 0
    for line in f:
        puzzle = Puzzle(line.split()[1], line.split()[0], None)
        length, seconds = time_solve(puzzle)
        print("Line", current_line, ":", puzzle.get_content(), ",", length, "moves found in", seconds, "seconds.")
        current_line += 1
