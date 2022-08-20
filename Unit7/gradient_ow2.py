import sys


def a(x, y):
    return 4 * (x ** 2) - 3 * x * y + 2 * (y ** 2) + 24 * x - 20 * y


def b(x, y):
    return (1 - y) ** 2 + (x - y ** 2) ** 2


def one_d_minimize(f, left, right, tolerance):
    if abs(left - right) < tolerance:
        return (left + right) / 2
    x1, x2 = left + (right - left) / 3, left + 2 * (right - left) / 3
    first, second = f(x1), f(x2)
    return one_d_minimize(f, x1, right, tolerance) if first > second else one_d_minimize(f, left, x2, tolerance)


def a_prime_x(x, y):
    return 8 * x + 24 - 3 * y


def a_prime_y(x, y):
    return 4 * y - 3 * x - 20


def b_prime_x(x, y):
    return 2 * (x - y ** 2)


def b_prime_y(x, y):
    return -2 * (1 - y) - 4 * y * (x - y ** 2)


def minimum_pointing_vector(x, y, x_prime, y_prime):
    gradient = (x_prime(x, y), y_prime(x, y))
    return -1.0 * gradient[0], -1.0 * gradient[1]


def under_threshold(gradient: tuple):
    return gradient[0] ** 2 + gradient[1] ** 2 < (10 ** -6.7) ** 2


def closure(f, grade, pos):
    def inner(dis):
        x1 = pos[0] + grade[0] * dis
        y1 = pos[1] + grade[1] * dis
        return f(x1, y1)

    return inner


current_pos = [0.0, 0.0]
func = sys.argv[1]
funcs: tuple
if func == "A":
    funcs = (a_prime_x, a_prime_y)
    func_reference = a
else:
    funcs = (b_prime_x, b_prime_y)
    func_reference = b
lr = 0.001

g = minimum_pointing_vector(current_pos[0], current_pos[1], funcs[0], funcs[1])





while not under_threshold(g):
    print("gradient=", g, "current pos=", current_pos)
    g = minimum_pointing_vector(current_pos[0], current_pos[1], funcs[0], funcs[1])
    current_pos[0] = current_pos[0] + g[0] * lr
    current_pos[1] = current_pos[1] + g[1] * lr

    # OPTIMIZED
    closure_func = closure(func_reference, g, current_pos)
    lr = one_d_minimize(closure_func, -0.4, 0.4, 10 ** -8)
print("local minimum ~@", current_pos)
