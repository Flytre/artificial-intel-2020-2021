f = open("sudoku.txt", "r")
lines = f.read().splitlines()

puzzles = []
index = 0
for i in range(0, 50):
    index += 1
    puzzles.append([list(lines[ind]) for ind in range(index, index + 9)])
    index += 9


def print_puzzle(puzzle):
    for i in range(0, 9):
        for index in range(0, 9):
            print(puzzle[i][index], end=('  ' if index % 3 != 2 else ' | '))
        print('')
        if i % 3 == 2:
            print("-----------------------------")


def possibilities(puzzle, r, c):
    block_row = r // 3
    block_col = c // 3
    nums = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for row in range(block_row * 3, block_row * 3 + 3):
        for col in range(block_col * 3, block_col * 3 + 3):
            if puzzle[row][col] in nums:
                nums.remove(puzzle[row][col])
    for row in range(0, 9):
        if row == r:
            continue
        if puzzle[row][c] in nums:
            nums.remove(puzzle[row][c])

    for col in range(0, 9):
        if col == c:
            continue
        if puzzle[r][col] in nums:
            nums.remove(puzzle[r][col])

    return nums


def solve(puzzle):
    while True:
        solved = True
        for row in range(0, 9):
            for col in range(0, 9):
                if puzzle[row][col] == '0':
                    solved = False
                    break
        if solved:
            return
        print()
        print_puzzle(puzzle)
        for row in range(0, 9):
            for col in range(0, 9):
                if puzzle[row][col] != '0':
                    continue
                else:
                    possible = possibilities(puzzle, row, col)
                    if len(possible) == 1:
                        puzzle[row][col] = next(iter(possible))


for puzzle in puzzles:
    solve(puzzle)
    print_puzzle(puzzle)
