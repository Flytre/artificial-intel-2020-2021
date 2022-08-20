import csv
import math
import os

import numpy as np


def parse_data(file: str):
    d = list()
    with open(file, mode='r') as f:
        reader = csv.reader(f)
        data = list(reader)
    for pt in data:
        num = int(pt.pop(0))
        matrix = np.vectorize(lambda k: int(k) / 255)(np.array([pt]))
        m_out = np.zeros((1, 10))
        m_out[(0, num)] = 1
        d.append((m_out, matrix))
    return d


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


def error(activation, weights, biases, x, y):
    return 1 / 2 * np.sum(np.vectorize(lambda k: k ** 2)(y - p_net(activation, weights, biases, x)))


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


data = parse_data("mnist_test.csv")
network = network_from_file()
data2 = parse_data("mnist_train.csv")

num = 0
denom = 0
for line in data:
    out = np.zeros((1, 10))
    out[(0, np.argmax(p_net(sigmoid, network[0], network[1], line[1])))] = 1
    denom += 1
    if np.array_equal(out, line[0]):
        num += 1
print("Test set result", num, "/", denom)

num = 0
denom = 0
for line in data2:
    out = np.zeros((1, 10))
    out[(0, np.argmax(p_net(sigmoid, network[0], network[1], line[1])))] = 1
    denom += 1
    if np.array_equal(out, line[0]):
        num += 1
print("Train set result", num, "/", denom)
