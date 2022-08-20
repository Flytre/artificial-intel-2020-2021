import ast
import math
import random
import sys

import numpy as np


def int_to_bin(n: int, length: int):
    return tuple([int(ch) for ch in
                  '{message:{fill}{align}{width}}'.format(
                      message=str(bin(n))[2:],
                      fill='0',
                      align='>',
                      width=length,
                  )
                  ])


def truth_table(bits, n):
    outs = tuple(reversed(int_to_bin(n, 2 ** bits)))
    res = dict({int_to_bin(i, bits): outs[i] for i in range(0, 2 ** bits)})
    return res


def pretty_print_table(table):
    v = len(([k for k in table.keys()][0]))
    print(" ".join(list([str(i + 1) for i in range(0, v)])), "| O")
    print((3 + 2 * v) * "-")
    for key in reversed(sorted(table.keys())):
        print(" ".join([str(i) for i in key]), "|", table[key])


def step(t: int):
    return 1 if t > 0 else 0


def perceptron(activation, weight, bias, x):
    return np.vectorize(activation)((x @ weight) + bias)


def p_net(activation, weights, biases, x):
    a = x
    for i in range(1, len(weights)):
        a = perceptron(activation, weights[i], biases[i], a)
    return a


def sigmoid(t: float):
    return 1 / (1 + math.e ** -t)


def train_circle():
    max_acc = 0
    max_vals = [np.array([[2.3], [2.3], [2.3], [2.3]]), np.array([-3.5])]
    for radius in range(0, 100):
        for final_bias in range(0, 100):
            curr_acc = 0
            curr_vals = [-5 + radius / 10, -5 + final_bias / 10]
            w_list = [None, np.array([[-1, -1, 1, 1], [1, -1, 1, -1]]), np.array([[1], [1], [1], [1]])]
            b_list = [None, np.array([curr_vals[0], curr_vals[0], curr_vals[0], curr_vals[0]]),
                      np.array([curr_vals[1]])]
            # accuracy test
            for i in range(0, 100):
                x = random.random() * 2 - 1
                y = random.random() * 2 - 1
                should = math.sqrt(x ** 2 + y ** 2) < 1
                arr = np.array([x, y])
                if (p_net(sigmoid, w_list, b_list, arr) >= 0.5) == should:
                    curr_acc += 1
            if max_acc < curr_acc:
                max_acc = curr_acc
                max_vals = curr_vals
        print(radius, "%", max_vals, max_acc)


if len(sys.argv) == 1:  # CIRCLE
    w_list = [None, np.array([[-1, -1, 1, 1], [1, -1, 1, -1]]), np.array([[1], [1], [1], [1]])]
    b_list = [None, np.array([2.3, 2.3, 2.3, 2.3]), np.array([-3.5])]
    curr_acc = 0
    for i in range(0, 500):
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        if (p_net(sigmoid, w_list, b_list, np.array([x, y])) >= 0.5) == (math.sqrt(x ** 2 + y ** 2) < 1):
            curr_acc += 1
        else:
            print((x, y))
    print("accuracy = ", curr_acc / 500, "%")
elif len(sys.argv) == 2:  # XOR HAPPENS HERE
    inp = ast.literal_eval(sys.argv[1])
    w_list = [None, np.array([[1, -1], [1, -1]]), np.array([[-1], [-1]])]
    b_list = [None, np.array([-1.5, 0.5]), np.array([0.5])]
    print(p_net(step, w_list, b_list, np.array([inp[0], inp[1]]))[0])
elif len(sys.argv) == 3:  # DIAMOND
    d_rad = 1
    w_list = [None, np.array([[-1, -1, 1, 1], [1, -1, 1, -1]]), np.array([[1], [1], [1], [1]])]
    b_list = [None, np.array([d_rad, d_rad, d_rad, d_rad]), np.array([-3.5])]
    arr = np.array([float(sys.argv[1]), float(sys.argv[2])])
    print("inside" if p_net(step, w_list, b_list, arr) == [1] else "outside")
