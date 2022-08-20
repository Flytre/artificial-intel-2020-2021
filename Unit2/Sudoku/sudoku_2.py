import math
import string
import sys
from collections import deque


# sudoku tile indices in this code start at 0 in the top left, then increase first left to right and then top to bottom.
# the terms index and tile are used interchangeably, though indices technically represent the position of a tile

class Constraints:
    sub_width: 3  # the size of each row in each block of the puzzle
    sub_height: 3  # the size of each column in each block of the puzzle
    size: 9  # the size of the entire row / column in the puzzle
    row: list  # a list of rows, each which is represented by a list of all indices in that row
    col: list  # a list of columns, each which is represented by a list of all indices in that column
    block: list  # a list of blocks, each which is represented by a list of all indices in that block
    squares: list  # a map of indices to lists. At each index is a list of all indices that index is constrained by.

    # I.e. index 0 is constrained by all elements of the first row, column, and block

    def __init__(self, big_size):
        self.sub_width = math.ceil(math.sqrt(big_size))
        self.sub_height = math.floor(math.sqrt(big_size))
        self.size = big_size
        self.row = list()
        self.col = list()
        self.block = list()
        self.squares = list()

        # Constraints - iterate through all tiles and figure out which row, column, and block they belong to
        for i in range(0, self.size):
            self.block.append(list())
        for i in range(0, self.size):
            r = list()
            c = list()
            for j in range(0, self.size):
                r.append(self.size * i + j)
                c.append(self.size * j + i)
                b_x = i // self.sub_height
                b_y = j // self.sub_width
                index = self.size * i + j
                block_num = b_x * self.sub_height + b_y
                self.block[block_num].append(index)
            self.row.append(r)
            self.col.append(c)

        # Run the gen constraints method, which populates the squares list containing the list of tiles each
        # individual tile is constrained by.
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

    # Method to check what tiles the tile is constrained by
    def constrained_by(self, index):
        return self.squares[index]


# the charset represents what characters are used for the sudoku board. Starts 1-9 then goes to A-Z.
charset = list()
charset.extend(string.digits)
charset.extend(string.ascii_uppercase)
charset.pop(0)

constraints_by_size = dict()


# the board represents the state of the sudoku puzzle
class Board:
    size: int
    con: Constraints
    state: str
    chars: list
    possibles: list

    def __init__(self, state, parent=None, changed=-1):
        self.size = int(math.sqrt(len(state)))

        # only 1 constraints object is needed for each board size. Since multiple sudoku puzzles are solved at once,
        # pass around the same used-immutably constraints object for each one of the same size
        if self.size in constraints_by_size:
            self.con = constraints_by_size[self.size]
        else:
            self.con = Constraints(self.size)
            constraints_by_size[self.size] = self.con

        self.state = state
        self.chars = list()
        for i in range(0, self.size):
            self.chars.append(charset[i])

        if parent is None:
            self.possibles = list()
            for i in range(0, self.size ** 2):
                self.possibles.append(self.valid_tiles(i))
        else:
            self.possibles = parent.possibles.copy()
            self.update_possibles(changed)

    #  Used to update the possibles list when a tile is changed
    # 1. Get all the tiles constrained by the changed tile
    # 2. Re-calculate possible values for each of these tiles
    # 3. If it only has 1 possibility and the think_list (which represents the list of tiles with only 1 possibility
    #    remaining so they can be changed) is defined, add to the think_list
    # 4. return true if the puzzle could still be solved, false if it definitely can't be
    # Old comment: If you are setting the character at an index to a value from a PERIOD,
    # this will fix the possibilities list
    def update_possibles(self, index, think_list: deque = None):
        for i in self.con.constrained_by(index):
            valid_tiles = self.valid_tiles(i)
            if think_list is not None and len(valid_tiles) == 1 and valid_tiles is not "-":
                think_list.append(i)
            if think_list is not None and len(valid_tiles) == 0:
                return False
            self.possibles[i] = valid_tiles
        return True

    # Add constrained values
    # Constraint Propagation deals with the idea that each row/col/block MUST have each value present once
    # Tells the puzzle to constraint by row, col, and block
    def constrained(self):
        self.constrain(self.con.row)
        self.constrain(self.con.col)
        self.constrain(self.con.block)

    # Constrain helper method / main login Takes in a list of lists, each sub-list representing a list of tiles that
    # are constrained by each other (i.e. [0-8] are in the same row and constrainted by each other)
    # All possible values for each given index are stored in the possibles list
    # 1. For each group
    #   a. Remove all values currently represented in the group
    #   b. For each unrepresented value:
    #       I. check if there's only 1 possible index in the group where that value can go
    #       II. if there is, set that index to the value
    # 2. If any changes have been made, forward think
    # 3. Return true if the board could still be possible to solve, and false if its definitely impossible
    #           For example, if a tile has no possible values left
    def constrain(self, constrain_type: list):
        changes = False
        for group in constrain_type:
            chars = self.chars.copy()
            for index in group:
                if self.state[index] in chars:
                    chars.remove(self.state[index])
            for char in chars:
                valid_ct = 0
                valid_index = 0
                for index in group:
                    if char in self.possibles[index]:
                        valid_ct += 1
                        valid_index = index
                if valid_ct == 1:
                    self.state = self.state[:valid_index] + char + self.state[valid_index + 1:]
                    solvable = self.update_possibles(valid_index)
                    changes = True
                    if not solvable:
                        return False
        if changes:
            return self.forward_think()
        return True

    # pretty print the board state
    def print(self):
        for i in range(0, self.size):
            for index in range(0, self.size):
                print(self.state[i * self.size + index], end=('  ' if index % 3 != 2 else ' | '))
            print('')
            if i % 3 == 2:
                print("-----------------------------")

    # returns the count of each value in the puzzle as a dict (for example, A: 5, B: 2, C: 3)
    def num_each(self):
        res = dict()
        for char in self.state:
            if char in res:
                res[char] += 1
            else:
                res[char] = 1
        return res

    # same as get_sorted_values as a comprehension
    def valid_tiles(self, period):
        if self.state[period] is not '.':
            return "-"
        invalid: list = list([self.state[x] for x in self.con.constrained_by(period)])
        return "".join(list([x for x in self.chars if x not in invalid]))

    # Forward thinking! - Filling in tiles with only 1 possible value
    # All possible values for each given index are stored in the possibles list
    # think_list represents all indices which only have 1 possible value
    # For each value in think list:
    #   => Set the value of that tile to only possible value
    #   => Update constraints now that that index has a value
    #   => If changes have been made, run constraint propagation
    #   => Return true if the board could still be possible to solve, and false if its definitely impossible
    #           For example, if a tile has no possible values left
    def forward_think(self):
        changes = False
        think_list = deque()
        for i in range(0, len(self.state)):
            if len(self.possibles[i]) == 0:
                return False
            if len(self.possibles[i]) == 1 and self.possibles[i] is not '-':
                think_list.append(i)
        while len(think_list) > 0:
            next_index = think_list.popleft()
            if self.possibles[next_index] == '-':
                continue
            self.state = self.state[:next_index] + self.possibles[next_index] + self.state[next_index + 1:]
            changes = True
            solvable = self.update_possibles(next_index, think_list)
            if not solvable:
                return False

        if changes:
            return self.constrained()
        return True


# returns all the possible values that can go at the index represented by period
def valid_values_at(board, index):
    invalid: set = board.con.constrained_by(index)
    possibles: set = board.chars
    for tile in invalid:
        if board.state[tile] in possibles:
            possibles.remove(board.state[tile])
    return list(possibles)


# backtracking core
# 1. if solved return the board
# 2. find the next blank on the board
# 3. loop through each valid value until one is the correct value and returns a solved board
# 4. if there is no valid value, return None
def backtrack(board: Board):
    if '.' not in board.state:
        return board
    period = get_next(board)
    for attempt in valid_values_at(board, period):

        # replace the board state with the modified one
        new_state = board.state[:period] + attempt + board.state[period + 1:]

        child = Board(new_state, board, period)
        solvable = child.forward_think()  # calls forward thinking and constraint propagation

        if solvable:
            result = backtrack(child)
            if result is not None:
                return result
    return None


# returns the next index to look at. Finds all blanks on the board, then retrieves the one where the least possible
# values can go.
def get_next(board: Board):
    periods = list(i for i in range(0, len(board.state)) if board.state[i] == '.')
    min_index: int = periods[0]
    min_val: int = len(board.possibles[min_index])

    for index in periods:
        if len(board.possibles[index]) < min_val:
            min_index = index
            min_val = len(board.possibles[min_index])
    return min_index

# with open(sys.argv[1]) as f:
#     for line in f:
#         b = Board(line.split('\n')[0])
#         print(backtrack(b).state)
