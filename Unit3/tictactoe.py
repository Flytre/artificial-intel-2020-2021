import sys


def winner(board: str, player: str):
    return check_rows(board, player) or check_cols(board, player) or check_diagonals(board, player)


def check_rows(board: str, player: str):
    for i in range(0, 3):
        bl = True
        for j in range(i * 3, (i + 1) * 3):
            if board[j] != player:
                bl = False
                break
        if bl:
            return True
    return False


def check_cols(board: str, player: str):
    for i in range(0, 3):
        bl = True
        for j in range(i, 9, 3):
            if board[j] != player:
                bl = False
                break
        if bl:
            return True
    return False


def check_diagonals(board: str, player: str):
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True
    return False


def score(board: str):
    if winner(board, "X"):
        return 1
    if winner(board, "O"):
        return -1
    return 0


def is_over(board: str):
    return ("." not in board) or (score(board) != 0)


def possible_moves(board: str, turn: str):
    result = set()
    for i in range(0, 9):
        if board[i] == ".":
            result.add(board[0:i] + turn + board[i + 1: 9])
    return result


def total_games(board: str, turn: str, final_boards: set):
    moves = possible_moves(board, turn)
    states = 0
    for move in moves:
        if is_over(move):
            final_boards.add(move)
            states += 1
        else:
            states += total_games(move, "O" if turn == "X" else "X", final_boards)
    return states


def max_step(board: str):
    if is_over(board):
        return score(board)
    results = list()
    for next_board in possible_moves(board, "X"):
        results.append(min_step(next_board))
    return max(results)


def letter(score: int, letter: str):
    if score == -1:
        return "L" if letter == "X" else "W"
    if score == 0:
        return "D"
    if score == 1:
        return "W" if letter == "X" else "L"


def max_move(board: str):
    if is_over(board):
        return board
    results = list()
    results_2 = list()
    for next_board in possible_moves(board, "X"):
        results.append(min_step(next_board))
        results_2.append(next_board)

    for i in range(0, len(results)):
        print(results_2[i], letter(results[i], "X"))

    max_val = max(results)
    index = results.index(max_val)
    return results_2[index]


def min_move(board: str):
    if is_over(board):
        return board
    results = list()
    results_2 = list()
    for next_board in possible_moves(board, "O"):
        results.append(max_step(next_board))
        results_2.append(next_board)

    for i in range(0, len(results)):
        print(results_2[i], letter(results[i], "O"))

    max_val = min(results)
    index = results.index(max_val)
    return results_2[index]


def min_step(board: str):
    if is_over(board):
        return score(board)
    results = list()
    for next_board in possible_moves(board, "O"):
        results.append(max_step(next_board))
    return min(results)


def print2(board: str):
    for i in range(0, 3):
        for index in range(0, 3):
            print(board[i * 3 + index], end=(' | ' if index % 3 != 2 else ' '))
        print('')
        if i != 2:
            print('-----------')


# result = set()
# print(total_games(".........", "X", result))
# print(len(result))
#
# win_5: int = 0
# win_6: int = 0
# win_7: int = 0
# win_8: int = 0
# win_9: int = 0
# draw: int = 0
#
# for r in result:
#     scr = score(r)
#     if scr == 0:
#         draw += 1
#         continue
#     moves = 9 - r.count(".")
#     if moves == 5:
#         win_5 += 1
#     if moves == 6:
#         win_6 += 1
#     if moves == 7:
#         win_7 += 1
#     if moves == 8:
#         win_8 += 1
#     if moves == 9:
#         win_9 += 1
# print("5", win_5)
# print("6", win_6)
# print("7", win_7)
# print("8", win_8)
# print("9", win_9)
# print("draw", draw)


game = sys.argv[1]
player = "X"
ai = "O"
turn = ai
print2(game)
if game.count(".") == 9:
    player = input("Which piece would you like to play (X/O)")
    ai = "O" if player == "X" else "X"
    turn = "X"
else:
    moves = 9 - game.count(".")
    ai = "X" if moves % 2 == 0 else "O"
    player = "O" if ai == "X" else "X"
    turn = ai
while not is_over(game):
    if turn == ai:
        print("Calculating...")
        if ai == "O":
            game = min_move(game)
        else:
            game = max_move(game)
        turn = player
        print("")
        print2(game)
        if is_over(game):
            break
    if turn == player:
        i: int = -1
        while i > 8 or i < 0 or game[i] != ".":
            i = int(input("Which tile would you like to play on (0-8)"))
        game = game[0:i] + player + game[i + 1: 9]
        print("")
        print2(game)
        turn = ai
lt = letter(score(game), player)
if lt == "D":
    print("Draw!")
if lt == "W":
    print("You won!")
if lt == "L":
    print("I won!")
