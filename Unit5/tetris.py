import sys

piece_dict = dict()
piece_dict["I"] = {"#   #   #   #   ", "####            "}
piece_dict["O"] = {"####"}
piece_dict["T"] = {" # ###   ", "#  ## #  ", "### #    ", " # ##  # "}
piece_dict["S"] = {" ####    ", "#  ##  # "}
piece_dict["Z"] = {"##  ##   ", " # ## #  "}
piece_dict["J"] = {"#  ###   ", "## #  #  ", "###  #   ", " #  # ## "}
piece_dict["L"] = {"  ####   ", "#  #  ## ", "####     ", "##  #  # "}


def print_piece(piece: str):
    sz = int(len(piece) ** 0.5)
    for count in range(sz):
        print(' '.join(piece[count * sz: (count + 1) * sz]))
    print("----")


def possible_columns(piece: str):
    sz = int(len(piece) ** 0.5)
    mi, mx = 10000, -1
    for col in range(0, sz):
        for row in range(0, sz):
            index = col + row * sz
            if piece[index] == "#":
                if col < mi:
                    mi = col
                if col > mx:
                    mx = col
    diff = mx - mi
    return list([i for i in range(0, Board.width - diff)])


class Board:
    width = 10
    height = 20

    def __init__(self, inp: str):
        self.vals = list()
        self.points = 0
        self.game_over = False
        for char in inp:
            self.vals.append(char)

    @staticmethod
    def to_index(x: int, y: int):
        return x + y * Board.width

    @staticmethod
    def to_x_y(i: int):
        return i % Board.width, i // Board.width

    def eliminate_filled_rows(self):
        to_rm = list()
        for row in range(0, Board.height):
            rm = True
            for col in range(0, Board.width):
                if self.vals[Board.to_index(col, row)] != "#":
                    rm = False
                    break
            if rm:
                to_rm.append(row)
        for row in to_rm:
            self.eliminate_row(row)
        if len(to_rm) == 1:
            self.points += 40
        if len(to_rm) == 2:
            self.points += 100
        if len(to_rm) == 3:
            self.points += 300
        if len(to_rm) == 4:
            self.points += 1200

    def eliminate_row(self, row: int):
        start_of_row = Board.to_index(0, row)
        for i in range(start_of_row - 1, -1, -1):
            self.vals[i + 10] = self.vals[i]
        for i in range(0, Board.width):
            self.vals[i] = " "

    def print(self):
        if self.game_over:
            print("GAME OVER")
            return
        print("=======================")
        for count in range(Board.height):
            print("|", ' '.join(self.vals[count * Board.width: (count + 1) * Board.width]), "|", "", count)
        print("=======================")

    def ugly_print(self):
        if self.game_over:
            return "GAME OVER"
        else:
            return "".join(self.vals)

    def add_piece(self, piece: str, col_offset: int):
        row_offset = 0
        not_found = True
        while not_found:
            indices = self.get_indices(piece, row_offset, col_offset)

            error = any([True for i in indices if i < 0 or self.vals[i] == "#"])
            if error:
                self.game_over = True
                return
            shifted = Board.shift_indices_down(indices)
            not_found = not any([i >= Board.width * Board.height or self.vals[i] == "#" for i in shifted])
            if not_found:
                row_offset += 1
        for index in self.get_indices(piece, row_offset, col_offset):
            self.vals[index] = "#"
        self.eliminate_filled_rows()

    def get_indices(self, piece: str, row_offset: int, col_offset: int):
        sz = int(len(piece) ** 0.5)
        return set(
            [Board.to_index(i % sz + col_offset, i // sz + row_offset) for i in range(0, len(piece)) if
             piece[i] == "#"])

    @staticmethod
    def shift_indices_down(indices: set):
        res = set()
        for val in indices:
            res.add(val + Board.width)
        return res


f = open("tetrisout.txt", "w")

test = sys.argv[1]
for key in piece_dict:
    for val in piece_dict[key]:
        for col in possible_columns(val):
            board = Board(test)
            board.add_piece(val, col)
            f.write(board.ugly_print() + "\n")
f.close()
