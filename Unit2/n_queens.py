import random
import time


def next_unassigned(state):
    return len(state[1])


def get_available_spaces(state, row):
    res = list()
    for col in range(0, state[0]):
        if col in state[1]:
            continue
        conflict = False
        for queen_row in range(0, row):
            queen_col = state[1][queen_row]
            if abs(queen_col - col) == abs(queen_row - row):
                conflict = True
                break
        if not conflict:
            res.append(col)
    random.shuffle(res)
    return res


def goal_state(state):
    return len(state[1]) == state[0]


def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if 0 <= left == state[compare]:
                print(var, "left", compare)
                return False
            if len(state) > right == state[compare]:
                print(var, "right", compare)
                return False
    return True


def csp_backtrack(state):
    if goal_state(state):
        return state
    row = next_unassigned(state)
    for col in get_available_spaces(state, row):
        new_state = (state[0], state[1].copy())
        new_state[1].append(col)
        result = csp_backtrack(new_state)
        if result is not None:
            return result
    return None


def get_conflicts(state):
    conflicts = 0
    for index in range(0, len(state[1])):
        conflicts += get_conflicts_row(state, index)
    return conflicts


def get_conflicts_row(state, row):
    col = state[1][row]
    state[1][row] = -1
    conflict = 0
    conflict += state[1].count(col)
    for queen_row in range(0, len(state[1])):
        queen_col = state[1][queen_row]
        if abs(queen_col - col) == abs(queen_row - row):
            conflict += 1
    state[1][row] = col
    return conflict


def optimize_row_conflicts(state, row):
    best_col = start_col = state[1][row]
    best_col_conflicts = 1000000000
    for possible_col in range(0, len(state[1])):
        state[1][row] = possible_col
        conflicts = get_conflicts_row(state, row)

        if conflicts < best_col_conflicts or (conflicts <= best_col_conflicts and best_col == start_col):
            best_col_conflicts = conflicts
            best_col = possible_col
    state[1][row] = best_col


def inc_repair(state):
    conflicts = get_conflicts(state)
    while conflicts > 0:
        for r in range(0, state[0]):
            optimize_row_conflicts(state, r)
            conflicts = get_conflicts(state)
            if conflicts == 0:
                return
        print(state, "conflicts=", conflicts)


def gen_board(size):
    x = list([i for i in range(0, size)])
    random.shuffle(x)
    return size, x

start = time.perf_counter()

solution = csp_backtrack((31,[]))
print("Backtracking Solution:", solution, "Is Valid?", test_solution(solution[1]))

print()

solution = csp_backtrack((32,[]))
print("Backtracking Solution:", solution, "Is Valid?", test_solution(solution[1]))

print()

stater = gen_board(31)
print("Incrmental Repair:")
print("Inital: ", stater, "conflicts=", get_conflicts(stater))
inc_repair(stater)
print("Solution:", stater, "Is Valid?", test_solution(solution[1]))

print()
stater = gen_board(32)
print("Incrmental Repair:")
print("Inital: ", stater, "conflicts=", get_conflicts(stater))
inc_repair(stater)
print("Solution:", stater, "Is Valid?", test_solution(solution[1]))


end = time.perf_counter()

print()
print("Time:", (end - start))
