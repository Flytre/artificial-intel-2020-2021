import sys
from enum import Enum

from typing import List, Set, Tuple


class Token(Enum):
    WHITE = "o"
    BLACK = "x"
    BLANK = "."

    def get_opposite(self):
        if self == Token.BLANK:
            raise Exception("Cannot get opposite of BLANK Token")
        return Token.BLACK if self == Token.WHITE else Token.WHITE

    @staticmethod
    def get_token(string: str):
        if string == "o":
            return Token.WHITE
        if string == "x":
            return Token.BLACK
        if string == ".":
            return Token.BLANK
        raise Exception("Cannot get Token for " + string)


class Board:
    tokens: list
    cache: dict

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.cache = dict()

    def __str__(self):
        result: str = ""
        for i in range(0, 8):
            for j in range(0, 8):
                result += self.tokens[i * 8 + j].value
            result += "\n"
        return result

    def ugly_print(self):
        result: str = ""
        for i in range(0, 64):
            result += self.tokens[i].value
        return result

    @staticmethod
    def create_from_string(string: str):
        result = list()
        for char in string:
            result.append(Token.get_token(char))
        return Board(result)

    @staticmethod
    def index_to_xy(i: int) -> Tuple[int, int]:
        return i % 8, i // 8

    @staticmethod
    def xy_to_index(x: int, y: int) -> int:
        return x + y * 8

    @staticmethod
    def in_bounds(x: int, y: int):
        return 0 <= x < 8 and 0 <= y < 8

    def tiles_with_token(self, token: Token) -> Set[int]:
        return set(i for i in range(0, 64) if self.tokens[i] == token)

    def possible_moves(self, token: Token) -> Set[int]:

        if token in self.cache:
            return self.cache[token]

        squares = self.tiles_with_token(token)
        result = set()

        while len(squares) > 0:
            pos_x, pos_y = Board.index_to_xy(squares.pop())
            self.add_movable_squares_to_set(pos_x, pos_y, token, Token.BLANK, result)
        self.cache[token] = result
        return result

    def add_movable_squares_to_set(self, pos_x: int, pos_y: int, token: Token, end_token: Token, result: set,
                                   funcs=None):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                r: int = self.try_move(pos_x, pos_y, lambda x, y: (x + i, y + j), token, end_token)
                if r != -1:
                    result.add(r)
                    if funcs is not None:
                        funcs.add((i, j))

    def try_move(self, x: int, y: int, func, token: Token, end_token: Token) -> int:
        n_x, n_y = func(x, y)
        if not Board.in_bounds(n_x, n_y) or self.tokens[Board.xy_to_index(n_x, n_y)] != token.get_opposite():
            return -1
        while Board.in_bounds(n_x, n_y) and self.tokens[Board.xy_to_index(n_x, n_y)] == token.get_opposite():
            n_x, n_y = func(n_x, n_y)
        if Board.in_bounds(n_x, n_y) and self.tokens[Board.xy_to_index(n_x, n_y)] == end_token:
            return Board.xy_to_index(n_x, n_y)
        return -1

    def move(self, index: int, end_token: Token):
        result = set()
        funcs = set()
        x, y = Board.index_to_xy(index)
        self.add_movable_squares_to_set(x, y, end_token, end_token, result, funcs)
        copy: Board = Board(self.tokens.copy())
        copy.tokens[Board.xy_to_index(x, y)] = end_token
        while len(funcs) > 0:
            func = funcs.pop()
            n_x, n_y = x, y
            while Board.xy_to_index(n_x, n_y) not in result:
                n_x, n_y = n_x + func[0], n_y + func[1]
                copy.tokens[Board.xy_to_index(n_x, n_y)] = end_token
        return copy


def find_next_move(board_string, player_string, depth):
    board = Board.create_from_string(board_string)
    player = Token.get_token(player_string)
    if player == Token.WHITE:
        return max_move(board, player, 0, depth, -10000, 10000)
    else:
        return min_move(board, player, 0, depth, -10000, 10000)


def score_mobi(board: Board, game_stage):
    black = len(board.possible_moves(token=Token.BLACK))
    white = len(board.possible_moves(token=Token.WHITE))
    x = white - black

    if black <= 3 and game_stage < 50:
        x += 20

    if black <= 2 and game_stage < 50:
        x += 10

    if white <= 3 and game_stage < 50:
        x -= 20

    if white <= 2 and game_stage < 50:
        x -= 10

    return x


def closest_corner(i: int):
    x, y = Board.index_to_xy(i)
    corners = {0, 7, 63, 56}
    min_val = 10000
    min_corner = 0
    for corner in corners:
        cx, cy = Board.index_to_xy(corner)
        val = (cx - x) ** 2 + (cy - y) ** 2
        if val < min_val:
            min_val = val
            min_corner = corner
    return min_corner


def score_raw_tokens(board: Board):
    score = 0
    for token in board.tokens:
        if token == Token.WHITE:
            score += 1
        if token == Token.BLACK:
            score -= 1
    return score


def score_board(board: Board):
    game_stage: int = sum([1 for i in board.tokens if i != Token.BLANK])

    if game_stage < 20:
        return score_mobi(board, game_stage) * 3 + score_raw_tokens(board)

    score = score_mobi(board, game_stage) * 4
    score += score_raw_tokens(board) if game_stage < 50 else score_raw_tokens(board) * 8

    for i in range(0, 64):
        x, y = Board.index_to_xy(i)
        if x == 0 or y == 0 or x == 7 or y == 7 or (abs(x) == abs(y) == 1) or (abs(x) == abs(y) == 7):
            token = board.tokens[i]
            corner = closest_corner(i)

            # grant extra points for adjacent tiles if it is the same color
            # grant extra points to walls
            # grant points for sandwhiched discs (surrounded on 8 sides)

            if token == Token.WHITE:
                score += -9 if not board.tokens[corner] == Token.WHITE else 2
            if token == Token.BLACK:
                score += 9 if not board.tokens[corner] == Token.BLACK else -2
    corners = {0, 7, 63, 56}
    for corner in corners:
        token = board.tokens[corner]
        white_could_move = corner in board.possible_moves(token=Token.WHITE)
        if token == Token.BLACK:
            score -= 50
        if token == Token.WHITE:
            score += 50
        if white_could_move:
            score += 20
    return score


def max_step(board: Board, player: Token, current_depth: int, target_depth: int, alpha: int, beta: int):
    if current_depth == target_depth:
        return score_board(board)
    results = list()
    moves = board.possible_moves(player)
    for next_board in moves:
        score = min_step(board.move(next_board, player), player.get_opposite(), current_depth + 1, target_depth, alpha,
                         beta)
        results.append(score)
        if score > alpha:
            alpha = score
        if alpha >= beta:
            break

    if len(moves) == 0:
        return 10000 + score_raw_tokens(board) if hit_75(board) > 0 else -10000 + score_raw_tokens(board)

    return max(results)


def hit_75(board: Board):
    black = len(board.tiles_with_token(token=Token.BLACK))
    white = len(board.tiles_with_token(token=Token.WHITE))
    return black / (black + white) > 0.75


def min_step(board: Board, player: Token, current_depth: int, target_depth: int, alpha: int, beta: int):
    if current_depth == target_depth:
        return score_board(board)
    results = list()
    moves = board.possible_moves(player)
    for next_board in moves:
        score = max_step(board.move(next_board, player), player.get_opposite(), current_depth + 1, target_depth, alpha,
                         beta)
        results.append(score)
        if score < beta:
            beta = score
        if alpha >= beta:
            break
    if len(moves) == 0:
        return -10000 + score_raw_tokens(board) if hit_75(board) > 0 else 10000 + score_raw_tokens(board)

    return min(results)


def max_move(board: Board, player: Token, current_depth: int, target_depth: int, alpha: int, beta: int):
    if current_depth == target_depth:
        return score_board(board)
    results = list()
    results_2 = list()
    for next_board in board.possible_moves(player):
        score = min_step(board.move(next_board, player), player.get_opposite(), current_depth + 1, target_depth, alpha,
                         beta)
        if score > alpha:
            alpha = score
        results.append(score)
        results_2.append(next_board)
        if alpha >= beta:
            break

    max_val = max(results)
    index = results.index(max_val)
    return results_2[index]


def min_move(board: Board, player: Token, current_depth: int, target_depth: int, alpha: int, beta: int):
    if current_depth == target_depth:
        return score_board(board)
    results = list()
    results_2 = list()
    for next_board in board.possible_moves(player):
        score = max_step(board.move(next_board, player), player.get_opposite(), current_depth + 1, target_depth, alpha,
                         beta)
        if score < beta:
            beta = score
        results.append(score)
        results_2.append(next_board)
        if alpha >= beta:
            break

    max_val = min(results)
    index = results.index(max_val)
    return results_2[index]


board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(15):  # 15 is arbitrary; a depth that your code won't reach, but infinite loops crash the grader
    print(find_next_move(board, player, depth))
    depth += 1

# class Strategy():
#     logging = True  # Optional
#
#     def best_strategy(self, board, player, best_move, still_running):
#         depth = 1
#         for count in range(
#                 15):  # 15 is arbitrary; a depth that your code won't reach, but infinite loops crash the grader
#             best_move.value = find_next_move(board, player, depth)
#             depth += 1
