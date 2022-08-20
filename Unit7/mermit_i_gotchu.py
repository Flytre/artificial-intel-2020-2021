import math

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


def one_matrix(r: int, c: int):
    return np.vectorize(lambda k: k + 1)(np.zeros((r, c)))


def create_network_rand(architecture: list):
    w_list = list()
    b_list = list()
    w_list.append(None)
    b_list.append(None)
    for i in range(0, len(architecture) - 1):
        w_list.append(rand_matrix(architecture[i], architecture[i + 1]))
    for i in range(1, len(architecture)):
        b_list.append(rand_matrix(1, architecture[i]))
    return w_list, b_list


def create_network_ones(architecture: list):
    w_list = list()
    b_list = list()
    w_list.append(None)
    b_list.append(None)
    for i in range(0, len(architecture) - 1):
        w_list.append(one_matrix(architecture[i], architecture[i + 1]))
    for i in range(1, len(architecture)):
        b_list.append(one_matrix(1, architecture[i]))
    return w_list, b_list


weights, bias = create_network_ones([3, 2, 1, 1])
# back_propagate(sigmoid, sigmoid_prime, weights, bias, np.array([[0, 1, 1]]), np.array([[1]]), 0.1, False)
# print("Weights:", weights)
# print("Bias:", bias)
print(p_net(sigmoid, weights, bias, np.array([[0, 1, 1]])))
