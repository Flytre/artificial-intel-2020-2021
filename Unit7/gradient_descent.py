import sys


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
    return gradient[0] ** 2 + gradient[1] ** 2 < (10 ** -8) ** 2


current_pos = [0.0, 0.0]
func = sys.argv[1]
funcs: tuple
if func == "A":
    funcs = (a_prime_x, a_prime_y)
else:
    funcs = (b_prime_x, b_prime_y)
lr = 0.001

g = minimum_pointing_vector(current_pos[0], current_pos[1], funcs[0], funcs[1])

while not under_threshold(g):
    print("gradient=", g, "current pos=", current_pos)
    g = minimum_pointing_vector(current_pos[0], current_pos[1], funcs[0], funcs[1])
    print(g)
    current_pos[0] = current_pos[0] + g[0] * lr
    current_pos[1] = current_pos[1] + g[1] * lr
print("local minimum ~@", current_pos)
