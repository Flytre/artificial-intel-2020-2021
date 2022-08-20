import math
import random
import sys

import numpy as np


def sigmoid(t: float):
    return 1 / (1 + math.e ** -t)


def sigmoid_prime(t: float):
    return sigmoid(t) * (1 - sigmoid(t))


def perceptron(activation, weight, bias, x):
    return np.vectorize(activation)((x @ weight) + bias)


def p_net(activation, weights, biases, x):
    a = x
    for i in range(1, len(weights)):
        a = perceptron(activation, weights[i], biases[i], a)
    return a


def back_propagate(activation, activation_prime, weights, biases, x, y, lr, debug):
    a_values = [x]
    dot_values = [None]
    deltas = [None] * len(weights)

    # Forward propagate
    for i in range(1, len(weights)):
        dot_values.append((a_values[i - 1] @ weights[i]) + biases[i])
        a_values.append(np.vectorize(activation)(dot_values[i]))

    # Delta Values
    delta_iter = len(weights) - 1
    deltas[delta_iter] = np.vectorize(activation_prime)(dot_values[delta_iter]) * (y - a_values[delta_iter])
    while delta_iter >= 2:
        delta_iter -= 1
        dot = deltas[delta_iter + 1] @ weights[delta_iter + 1].transpose()
        deltas[delta_iter] = np.vectorize(activation_prime)(dot_values[delta_iter]) * dot

    # Update matrices
    for i in range(1, len(weights)):
        biases[i] = biases[i] + lr * deltas[i]
        weights[i] = weights[i] + lr * a_values[i - 1].transpose() @ deltas[i]

    if debug:
        print("In:", x, "--> Out:", a_values[len(a_values) - 1])


def error(activation, weights, biases, x, y):
    return 1 / 2 * np.sum(np.vectorize(lambda k: k ** 2)(y - p_net(activation, weights, biases, x)))


def rand():
    return random.uniform(-1, 1)


# inp = np.array([[2, 3]])
# out = np.array([[0.8, 1]])
# w1 = np.array([[1, - .5], [1, .5]])
# b1 = np.array([[1, -1]])
# w2 = np.array([[1, 2], [-1, -2]])
# b2 = np.array([[-.5, .5]])
# w_list = [None, w1, w2]
# b_list = [None, b1, b2]
# print("ERROR", error(sigmoid, w_list, b_list, inp, out))
# print("\n>>>>PROPOGATE")
# print(w_list)
# back_propagate(sigmoid, sigmoid_prime, w_list, b_list, inp, out, 0.1, True)
# print("ERROR2", error(sigmoid, w_list, b_list, inp, out))


def sum():
    sum_pairs = list()
    sum_pairs.append((np.array([[0, 0]]), np.array([[0, 0]])))
    sum_pairs.append((np.array([[0, 1]]), np.array([[0, 1]])))
    sum_pairs.append((np.array([[1, 0]]), np.array([[0, 1]])))
    sum_pairs.append((np.array([[1, 1]]), np.array([[1, 0]])))
    w_list = [None, np.array([[rand(), rand()], [rand(), rand()]]), np.array([[rand(), rand()], [rand(), rand()]])]
    b_list = [None, np.array([[rand(), rand()]]), np.array([[rand(), rand()]])]

    for n in range(0, 10000):
        for i in range(0, len(sum_pairs)):
            back_propagate(sigmoid, sigmoid_prime, w_list, b_list, sum_pairs[i][0], sum_pairs[i][1], 0.1, True)


def rand_matrix(r: int, c: int):
    return np.vectorize(lambda k: k * 2 - 1)(np.random.rand(r, c))


def create_network(architecture: list):
    w_list = list()
    b_list = list()
    w_list.append(None)
    b_list.append(None)
    for i in range(0, len(architecture) - 1):
        w_list.append(rand_matrix(architecture[i], architecture[i + 1]))
    for i in range(1, len(architecture)):
        b_list.append(rand_matrix(1, architecture[i]))
    return w_list, b_list


def circle():
    w_list, b_list = create_network([2, 12, 4, 1])
    points = list()
    for i in range(0, 10000):
        points.append((random.random() * 2 - 1, random.random() * 2 - 1))
    for k in range(0, 1000):
        for i in range(0, 10000):
            x = points[i][0]
            y = points[i][1]
            output = 1 if (math.sqrt(x ** 2 + y ** 2) < 1) else 0
            lr = (output - p_net(sigmoid, w_list, b_list, np.array([x, y]))) ** 2
            back_propagate(sigmoid, sigmoid_prime, w_list, b_list, np.array([[x, y]]), np.array([[output]]), lr, False)
        curr_acc = 0
        for i in range(0, 10000):
            x = random.random() * 2 - 1
            y = random.random() * 2 - 1
            if (p_net(sigmoid, w_list, b_list, np.array([x, y])) >= 0.5) == (math.sqrt(x ** 2 + y ** 2) < 1):
                curr_acc += 1
        print("accuracy = ", curr_acc / 100, "%")


# letter = sys.argv[1]
#
# if letter == "C":
#     circle()
# elif letter == "S":
#     sum()

wx = [None, np.array([[-0.5851747036, -0.2028676204, 0.1671980617, 0.490376784, 0.7544195919, -0.0341590197,
                       -0.2041835257, -0.9751920518, -0.9235142868, 0.3741126759, -0.0403639582, 0.8718466114],
                      [0.5131505204, -0.1410270854, -0.2239976073, 0.8886740665, 0.1687178729, 0.0273212635,
                       -0.5362319371, -0.9458385018, -0.9745799925, -0.5418860736, 0.5342622086, -0.2223410407]]),
      np.array([[-0.7593345525, -0.7568596321, -0.6635663051, 0.0805886822],
                [-0.5313427589, -0.52563407, -0.8006068275, -0.1542713502],
                [0.5755827243, 0.6002641009, 0.4331567615, 0.1747739752],
                [-0.0835944849, -0.5494839232, -0.4715264258, -0.6970313816],
                [-0.7973837082, -0.8320910797, -0.9608044974, -0.5096990546],
                [0.9141299017, -0.7117856393, -0.1642721025, 0.8419619803],
                [-0.8051583505, 0.7732870512, -0.31432395, -0.8935336911],
                [-0.7798141405, 0.9295704214, 0.4478817105, 0.1580400818],
                [0.1363670402, 0.833654622, 0.5586216533, 0.0905834681],
                [0.8447616248, -0.8615182349, -0.056181907, 0.6337170584],
                [-0.8586824218, 0.9482480924, -0.9913104038, 0.947126683],
                [-0.9803933809, 0.8270059236, -0.0636516962, 0.7576219276]]),
      np.array([[0.3075111522], [0.9454202619], [-0.8305713872], [0.2740290206]])]
bx = [None, np.array([[-0.7686414716, 0.872089084, 0.6539091885, -0.6517597784, -0.0123602425, 0.5802893639,
                       0.1918695639, -0.0535542525, -0.0487181627, 0.8679634269, 0.0799999869, 0.1527774084]]),
      np.array([[0.7607678704, -0.4217865293, 0.1032614521, 0.6482959997]]), np.array([[0.1942291772]])]
vec = np.array([[-0.24047362412859474, -0.09182909309222942]])
back_propagate(sigmoid, sigmoid_prime, wx, bx, vec, np.array([[0]]), 1, False)
print(wx)
print(bx)
