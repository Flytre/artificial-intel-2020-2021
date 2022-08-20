import copy
import sys


def area_check():
    return puzzle_height * puzzle_width == sum([rect[0] * rect[1] for rect in rectangles])


# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
puzzle = "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4".split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions
failed: bool = False
if not area_check():
    print("Containing rectangle incorrectly sized.")


class Block:
    x: int
    y: int
    width: int
    height: int
    x1: int
    y1: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x1 = x + width
        self.y1 = y + width

    # Checks whether a point lays inside the block
    def enclosed(self, x: float, y: float):
        return self.x < x < self.x1 and self.y < y < self.y1

    # Get the bounds of the rect
    def bounds(self):
        return self.x, self.x1, self.y, self.y1


class State:
    width: int
    height: int
    rects: list
    blocks: list

    def __init__(self, width, height, rects: list, blocks: list):
        self.width = width
        self.height = height
        self.rects = rects
        self.blocks = blocks

    def can_add(self, x: int, y: int, dims: tuple):
        for i in range(0, dims[0]):
            for j in range(0, dims[1]):
                px = x + 0.5 + i
                py = y + 0.5 + j
                for block in self.blocks:
                    if block.enclosed(px, py):
                        return False
        return True

    def children(self):
        block = Block(0, 0, 0, 0)
        if len(self.blocks) > 0:
            block = self.blocks[len(self.blocks) - 1]
        possibles = list()
        result = list()
        possibles.append((block.x, block.y1))
        if block.width != 0 or block.height != 0:
            possibles.append((block.x1, block.y))

        for possible in possibles:
            for r in self.rects:
                if self.can_add(possible[0], possible[1], r):
                    child_rects = copy.copy(self.rects)
                    child_rects.remove(r)
                    child_blocks = copy.copy(self.blocks)
                    child_blocks.append(Block(possible[0], possible[1], r[0], r[1]))
                    result.append(State(self.width, self.height, child_rects, child_blocks))
        return result


base = State(puzzle_width, puzzle_height, list(rectangles), list())
print(base.width, base.height, base.rects, base.blocks)
children = base.children()
for res in children:
    print(res.width, res.height, res.rects, res.blocks[0].bounds())
child = children[0]
print()
print(child.width, child.height, child.rects, child.blocks)
grandchildren = child.children()
for res in grandchildren:
    print(res.width, res.height, res.rects, res.blocks[0].bounds(), res.blocks[1].bounds())

# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
#
# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.
