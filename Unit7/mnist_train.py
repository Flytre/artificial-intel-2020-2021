import csv
import math
import os

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


def network_to_file(w_list: list, b_list: list):
    ct = 0
    try:
        os.mkdir("mnist")
    except OSError:
        pass
    for w in w_list:
        np.save("mnist/w_" + str(ct), w)
        ct += 1
    ct = 0
    for b in b_list:
        np.save("mnist/b_" + str(ct), b)
        ct += 1


def network_from_file():
    w_list = list()
    b_list = list()
    ct = 0
    while os.path.exists("mnist/w_" + str(ct) + ".npy"):
        w_list.append(np.load("mnist/w_" + str(ct) + ".npy", allow_pickle=True))
        ct += 1
    ct = 0
    while os.path.exists("mnist/b_" + str(ct) + ".npy"):
        b_list.append(np.load("mnist/b_" + str(ct) + ".npy", allow_pickle=True))
        ct += 1
    return w_list, b_list


def parse_data():
    d = list()
    with open("mnist_train.csv", mode='r') as f:
        reader = csv.reader(f)
        data = list(reader)
    for pt in data:
        num = int(pt.pop(0))
        matrix = np.vectorize(lambda k: int(k) / 255)(np.array([pt]))
        m_out = np.zeros((1, 10))
        m_out[(0, num)] = 1
        d.append((m_out, matrix))
    return d


network = network_from_file()
data = parse_data()
print("Starting main loop")
while True:
    for line in data:
        back_propagate(sigmoid, sigmoid_prime, network[0], network[1], line[1], line[0], 0.1, False)
    print("epoch")
    network_to_file(network[0], network[1])

