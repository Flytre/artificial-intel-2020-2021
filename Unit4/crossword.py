# NOTE: columns are on the x-axis and rows are on the y-axis: Increasing row increases y!
import math
import string
import sys
from collections import deque


class Block:
    x: int
    y: int
    horiz: bool
    length: int

    def __init__(self, x: int, y: int, horiz: bool, length: int):
        self.x = x
        self.y = y
        self.horiz = horiz
        self.length = length

    def __str__(self) -> str:
        return str(self.x) + ", " + str(self.y) + " horiz=" + str(self.horiz) + " length=" + str(self.length)

    def contains(self, x, y):
        if self.horiz:
            return y == self.y and self.x <= x < self.x + self.length
        else:
            return x == self.x and self.y <= y < self.y + self.length

    # Set of contained points
    def contained_points(self):
        result = set()
        if self.horiz:
            for i in range(self.x, self.x + self.length):
                result.add((i, self.y))
        else:
            for i in range(self.y, self.y + self.length):
                result.add((self.x, i))
        return result

    # List of contained points
    def contained_points_ordered(self):
        result = list()
        if self.horiz:
            for i in range(self.x, self.x + self.length):
                result.append((i, self.y))
        else:
            for i in range(self.y, self.y + self.length):
                result.append((self.x, i))
        return result

    # List of contained points in an inside out order
    def get_iterate_order(self):
        all_indices = list()
        if self.horiz:
            for i in range(self.x, self.x + self.length):
                all_indices.append((i, self.y))
        else:
            for i in range(self.y, self.y + self.length):
                all_indices.append((self.x, i))
        ret = list()
        first = self.length // 3
        second = (self.length * 2) // 3
        ret.extend([all_indices[i] for i in range(first, second)])
        ret.extend([all_indices[i] for i in range(0, first)])
        ret.extend([all_indices[i] for i in range(second, self.length)])
        return ret

    # At what index along block1 does point 2 intersect. For example
    # self = 1, 0 horiz=False length=4
    # block2 = 0, 2 horiz=True length=4
    # index = 2 because the 3rd segment of self intersects with block2
    def get_intersect_index(self, block2):
        points: set = block2.contained_points()
        self_points = self.contained_points_ordered()
        for i in range(0, len(self_points)):
            if self_points[i] in points:
                return i
        return -1


def constraint_sort(tup: tuple):
    return tup[0] - tup[1].length


def valid_word_sort(tup: tuple):
    return -tup[0]


last: bool = False


class Crossword:
    letters = list()
    width: int
    height: int
    hashtag_singleton = {"#"}
    letters_hashtag_collection = set([i for i in string.ascii_lowercase + "#"])
    added_words: set

    def __init__(self, width: int, height: int, letters: list, added_words: set):
        self.letters = letters
        self.width = width
        self.height = height
        self.added_words = added_words.copy()

    @staticmethod
    def parse_dim(dim: str):
        toggle = False
        x = y = ""
        end: int = len(dim) - 1
        for i in range(0, len(dim)):
            char = dim[i]
            if char.isnumeric():
                if toggle:
                    y += char
                else:
                    x += char
            else:
                if not toggle:
                    toggle = True
                else:
                    end = i
                    break
        return int(x), int(y), end

    def to_index(self, x: int, y: int):
        return x + y * self.width

    def to_x_y(self, i: int):
        return i % self.width, i // self.width

    @staticmethod
    def create_from_cli(cli):
        height, width, junk = Crossword.parse_dim(cli[1])
        letters = list(["-" for i in range(0, width * height)])
        crossword: Crossword = Crossword(width, height, letters, set())
        crossword.add_premade(cli)
        crossword.added_words = crossword.get_all_words_in_puzzle()
        crossword.fix_small_segments()

        for xy in crossword.get_disconnected_tiles():
            index = crossword.to_index(xy[0], xy[1])
            crossword.letters[index] = "#"
            crossword.letters[crossword.opposite_index(index)] = "#"

        return crossword

    def opposite_index(self, i):
        return (self.width * self.height) - 1 - i

    # add CLI premades, ie "H3x10#"
    def add_premade(self, cli):
        for i in range(4, len(cli)):
            backup = self.letters.copy()
            arg = cli[i]
            horiz: bool = arg[0] == "H" or arg[0] == "h"
            y, x, end = Crossword.parse_dim(arg[1:])
            left = arg[end + 1:]
            left = left.lower()
            if horiz:
                for j in range(0, len(left)):
                    self.letters[self.to_index(x, y) + j] = left[j]
                    if left[j] == "#":
                        self.letters[self.opposite_index(self.to_index(x, y) + j)] = "#"
            else:
                for j in range(0, len(left)):
                    self.letters[self.to_index(x, y + j)] = left[j]
                    if left[j] == "#":
                        self.letters[self.opposite_index(self.to_index(x, y + j))] = "#"
            if not self.is_connected():
                self.letters = backup

    # get words:
    def get_all_words_in_puzzle(self):
        blocks = self.get_blocks(Crossword.hashtag_singleton)
        filled_blocks = set()
        for block in blocks:
            if self.is_block_filled(block):
                filled_blocks.add(block)
        result = set()
        for block in filled_blocks:
            result.add("".join(self.get_char_list(block)))
        return result

    def get_all_connected_squares(self, x: int, y: int):
        to_visit = deque()
        visited = set()
        if self.letters[self.to_index(x, y)] != "#":
            visited = {(x, y)}
        to_visit.append((x, y))
        while len(to_visit) > 0:
            curr = to_visit.popleft()
            children = self.get_adjacent(curr[0], curr[1])
            for child in children:
                if child not in visited:
                    to_visit.append(child)
                    visited.add(child)
        return visited

    def is_connected(self):
        visited = self.get_all_connected_squares(0, 0)
        test = len(visited)
        for letter in self.letters:
            if letter == "#":
                test += 1
        return test == self.width * self.height

    # checks if all blanks are at least 3 wide horizontally / vertically ~ validity check
    def are_blanks_long_enough(self, chars: set):
        blocks = self.get_blocks(chars)
        for block in blocks:
            if block.length < 3:
                return False
        return True

    def get_adjacent(self, x: int, y: int):
        result = list()
        if self.in_bounds(x + 1, y) and self.letters[self.to_index(x + 1, y)] != "#":
            result.append((x + 1, y))
        if self.in_bounds(x - 1, y) and self.letters[self.to_index(x - 1, y)] != "#":
            result.append((x - 1, y))
        if self.in_bounds(x, y + 1) and self.letters[self.to_index(x, y + 1)] != "#":
            result.append((x, y + 1))
        if self.in_bounds(x, y - 1) and self.letters[self.to_index(x, y - 1)] != "#":
            result.append((x, y - 1))
        return result

    def in_bounds(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height

    # get a series of blocks that define the open space in a board
    def get_blocks(self, chars: set):
        blocks = list()
        for row in range(0, self.height):
            start = 0
            for col in range(0, self.width):
                val = self.letters[self.to_index(col, row)]
                if val in chars:
                    if col - start > 0:
                        blocks.append(Block(start, row, True, col - start))
                    start = col + 1
            if self.width - start > 0:
                blocks.append(Block(start, row, True, self.width - start))
        for col in range(0, self.width):
            start = 0
            for row in range(0, self.height):
                val = self.letters[self.to_index(col, row)]
                if val in chars:
                    if row - start > 0:
                        blocks.append(Block(col, start, False, row - start))
                    start = row + 1
            if self.height - start > 0:
                blocks.append(Block(col, start, False, self.height - start))
        return blocks

    def __str__(self):
        result: str = ""
        for i in range(0, self.height):
            for j in range(0, self.width):
                result += self.letters[i * self.width + j] + " "
            result += "\n"
        return result

    # arbitary block sort prioritizing longer, more central boards
    def block_sort(self, block: Block):
        base = -block.length * 1000
        val = self.width if block.horiz else self.height
        base += abs((block.x if block.horiz else block.y) - (val / 2))
        return base

    # get a list of all possible wall locations, best to worst
    def get_ordered_wall_list(self):
        blocks = self.get_blocks(Crossword.hashtag_singleton)
        blocks.sort(key=self.block_sort)
        start = blocks[0].length
        order = list()
        while start >= 0:
            order.extend(self.get_wall_moves_with_num_center(start, blocks))
            start -= 1
        order = list([i for n, i in enumerate(order) if i not in order[:n]])
        return order

    def add_walls(self, count: int):
        if count % 2 == self.width % 2 == self.height % 2 == 1:
            index = self.to_index(self.width // 2, self.height // 2)
            if self.letters[index] != "#":
                self.letters[index] = "#"
        current_walls = len([i for i in self.letters if i == "#"])
        result = self.add_walls_helper(count - current_walls)
        result.added_words = result.get_all_words_in_puzzle()
        return result

    def count_non_walls(self):
        return len([i for i in self.letters if i != "#"])

    def add_walls_helper(self, count: int):
        if count <= 0:
            return self
        if count == self.count_non_walls():
            for i in range(0, len(self.letters)):
                self.letters[i] = "#"
            return self
        for move in self.get_ordered_wall_list():
            state = Crossword(self.width, self.height, self.letters.copy(), self.added_words)
            index2 = (self.width * self.height) - 1 - move
            state.letters[move] = "#"
            state.letters[index2] = "#"
            result = state.add_walls_helper(count - 2)
            if result is not None:
                return result
        return None

    # used in calculating the best place for a wall, prioritizes central moves over edge moves
    def get_wall_moves_with_num_center(self, num: int, blocks: list):
        result = list()
        for block in blocks:
            if block.length < num:
                continue
            if block.horiz:
                pos1 = self.to_index(block.x + (num // 2), block.y)
                pos2 = self.to_index(block.x + block.length - 1 - (num // 2), block.y)
                if self.is_valid_square_to_add_wall(pos1):
                    result.append(pos1)
                if pos1 != pos2 and self.is_valid_square_to_add_wall(pos2):
                    result.append(pos2)
            else:
                pos1 = self.to_index(block.x, block.y + (num // 2))
                pos2 = self.to_index(block.x, block.y + block.length - 1 - (num // 2))
                if self.is_valid_square_to_add_wall(pos1):
                    result.append(pos1)
                if pos1 != pos2 and self.is_valid_square_to_add_wall(pos2):
                    result.append(pos2)
        return list([i for n, i in enumerate(result) if i not in result[:n]])

    # Returns whether after adding a wall to the specified indice the board will still be valid
    def is_valid_square_to_add_wall(self, index):
        if self.width % 2 == self.height % 2 == 1:
            if self.to_x_y(index) == (self.width // 2, self.height // 2):
                return False
        index2 = self.opposite_index(index)
        current: str = self.letters[index]
        current2: str = self.letters[index2]
        if current != "-" or current2 != "-":
            return False
        self.letters[index] = "#"
        self.letters[index2] = "#"
        val: bool = self.are_blanks_long_enough(Crossword.hashtag_singleton) and self.is_connected()
        self.letters[index] = current
        self.letters[index2] = current2
        return val

    # If the board is corrupted at the start due to blanks of less than 3, this method adds more walls to remove them
    def fix_small_segments(self):
        blocks = self.get_blocks(Crossword.hashtag_singleton)
        for block in blocks:
            if block.length < 3:
                for coord in block.get_iterate_order():
                    index = self.to_index(coord[0], coord[1])
                    self.letters[index] = "#"
                    self.letters[self.opposite_index(index)] = "#"
        if not self.are_blanks_long_enough(Crossword.hashtag_singleton):
            self.fix_small_segments()

    def get_disconnected_tiles(self):
        visited = set()
        biggest = set()
        for i in range(0, self.width * self.height):
            x, y = self.to_x_y(i)
            if (x, y) in visited:
                continue
            if self.letters[i] == "#":
                continue
            current = self.get_all_connected_squares(x, y)
            if len(current) > len(biggest):
                biggest = current
            visited = visited.union(current)
        return visited - biggest

    def set_blank(self, index: int):
        self.letters[index] = "-"
        self.letters[self.opposite_index(index)] = "-"

    # Part 2 master method
    def add_words(self, blocks: list):
        unfilled = self.get_unfilled_blocks(blocks)
        if len(unfilled) == 0:
            return self
        nxt = self.get_most_constrained_block(blocks)
        block_to_index = dict()
        block_to_pattern = dict()
        block_to_index_reverse = dict()
        points = nxt.contained_points()

        for block in blocks:
            if block == nxt:
                continue
            for point in points:
                if block.contains(point[0], point[1]):
                    block_to_index[block] = nxt.get_intersect_index(block)
                    block_to_pattern[block] = self.get_char_list(block)
                    block_to_index_reverse[block] = block.get_intersect_index(nxt)
                    continue
        words: list = self.get_sorted_valid_words(nxt, block_to_index, block_to_pattern, block_to_index_reverse)
        for word in words:
            nx = Crossword(self.width, self.height, self.letters.copy(), self.added_words)
            for i, x_y in enumerate(nxt.contained_points_ordered()):
                index = self.to_index(x_y[0], x_y[1])
                nx.letters[index] = word[i]
            nx.added_words.add(word)
            result = nx.add_words(blocks)
            if result is not None:
                return result
        return None

    # Checks if a block is fully filled with letters
    def is_block_filled(self, block: Block):
        for point in block.contained_points():
            if self.letters[self.to_index(point[0], point[1])] == "-":
                return False
        return True

    # Get only blocks not totally filled with letters
    def get_unfilled_blocks(self, blocks: list):
        result = list()
        for block in blocks:
            if not self.is_block_filled(block):
                result.append(block)
        return result

    # Get the pattern for a block, ie [-,t,a,-]
    def get_char_list(self, block: Block):
        result = list()
        for point in block.contained_points_ordered():
            index = self.to_index(point[0], point[1])
            result.append(self.letters[index])
        return result

    def get_most_constrained_block(self, blocks: list):
        result = list()
        for block in blocks:
            if self.is_block_filled(block):
                continue
            result.append(
                (len(dictionary.all_words_matching_pattern(self.get_char_list(block), self.added_words)), block))
        result.sort(key=constraint_sort)
        return result[0][1] if len(result) > 0 else None

    def get_sorted_valid_words(self, current: Block, block_to_index: dict, block_to_pattern: dict,
                               block_to_index_reverse: dict):
        words = dictionary.all_words_matching_pattern(self.get_char_list(current), self.added_words)
        result = list()

        for word in words:

            if word in self.added_words:
                continue

            bl = True
            heuristic = list()
            for block, index in block_to_index.items():
                pattern = block_to_pattern[block]
                pattern = pattern.copy()
                rev_index = block_to_index_reverse[block]
                pattern[rev_index] = word[index]
                i = len(dictionary.all_words_matching_pattern(pattern, self.added_words))
                if i == 0:
                    bl = False
                    break
                heuristic.append(i)
            if bl:
                result.append((geomean(heuristic), word))
                result.sort(key=valid_word_sort)
        result2 = list()
        for val in result:
            result2.append(val[1])
        return result2


def geomean(xs):
    return math.exp(math.fsum(math.log(x) for x in xs) / len(xs))


class Dict:
    raw_set: set
    sets_by_length: dict
    all_word_cache = dict
    valid_letters = {"a", "c", "d", "e", "h", "i", "l", "n", "o", "p", "r", "s", "t", "u"}

    def __init__(self, dictionary: str, max_len: int):
        with open(dictionary) as f:
            lines = [line.strip() for line in f]
            self.raw_set = set()
            for line in lines:
                if len(line) <= max_len:
                    lower = line.lower()
                    add = True
                    for char in lower:
                        if char not in self.valid_letters:
                            add = False
                            break
                    if add:
                        self.raw_set.add(line.lower())
            self.sets_by_length = dict()
            for word in self.raw_set:
                list2 = self.sets_by_length.get(len(word), set())
                list2.add(word)
                self.sets_by_length[len(word)] = list2
        self.all_word_cache = dict()

    def all_words_matching_pattern(self, pattern: list, blacklist: set):
        key = "".join(pattern)

        ls = self.sets_by_length[len(pattern)]

        if key in ls:
            return [key]

        if key in blacklist:
            return list()

        if key in self.all_word_cache:
            return self.all_word_cache[key]

        results = list()

        indices_to_check = set()
        for i in range(0, len(pattern)):
            char = pattern[i]
            if char != "-":
                indices_to_check.add(i)

        for word in ls:

            if word in blacklist:
                continue

            bl = True
            for i in indices_to_check:
                char = pattern[i]
                if char != word[i]:
                    bl = False
                    break
            if bl:
                results.append(word)

        self.all_word_cache[key] = results.copy()
        return results


args = sys.argv
height, width, junk = Crossword.parse_dim(args[1])
val = max(height, width)
dictionary = Dict(args[3], val)
crossword = Crossword.create_from_cli(args)
crossword = crossword.add_walls(int(args[2]))
# final = crossword.add_words(crossword.get_blocks(Crossword.hashtag_singleton))
print(crossword)
