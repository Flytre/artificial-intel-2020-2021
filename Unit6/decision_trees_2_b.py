import csv
import math
import random as random
import sys

import matplotlib.pyplot as plt


class Leaf:
    data: list
    output_header: str

    def __init__(self, data: list, header: str) -> None:
        self.data = data
        self.output_header = header
        self.output_value = data[0][header]


class Parent:
    def __init__(self, data: list, header: str):
        self.nodes = dict()
        self.factor = best_factor(data, header)
        split_data = dict()

        result_freq = dict()
        for pt in data:
            val = pt[header]
            if val not in result_freq:
                result_freq[val] = 1
            else:
                result_freq[val] = result_freq[val] + 1
        self.default = max(result_freq, key=result_freq.get)

        for pt in data:
            val = pt[self.factor]
            if val not in split_data:
                split_data[val] = list()
            split_data[val].append(pt)
        for key in split_data:
            if entropy(split_data[key], header) == 0:
                self.nodes[key] = Leaf(split_data[key], header)
            else:
                child_data = split_data[key]
                child_factor = best_factor(child_data, header)
                if len(set(pt[child_factor] for pt in child_data)) == 1:
                    self.nodes[key] = Leaf(child_data, header)
                else:
                    self.nodes[key] = Parent(child_data, header)

    def print(self):
        print(recursive_print(0, self))

    def __str__(self):
        return recursive_print(0, self)

    def get_expected_value(self, data_point):
        comparison_value = data_point[self.factor]

        if comparison_value not in self.nodes:
            return self.default

        next_val = self.nodes[comparison_value]
        if isinstance(next_val, Leaf):
            return next_val.output_value
        return next_val.get_expected_value(data_point)


def recursive_print(indent: int, parent: Parent):
    out = (" " * indent) + "* " + parent.factor + "?\n"
    for key in sorted(parent.nodes):
        if isinstance(parent.nodes[key], Leaf):
            out += (" " * (indent + 2)) + "* " + key + " --> " + parent.nodes[key].output_value + "\n"
        else:
            out += (" " * (indent + 2)) + "* " + key + "\n"
            out += recursive_print(indent + 4, parent.nodes[key])
    return out


def entropy(dataset: list, header: str):
    freq = dict()
    for pt in dataset:
        val = pt[header]
        freq[val] = freq[val] + 1 if val in freq else 1

    return -1 * sum(math.log2(freq[x] / len(dataset)) * (freq[x] / len(dataset)) for x in freq)


def expected_entropy(dataset: list, header: str, known_value: str):
    known_map = dict()
    freq = dict()
    for pt in dataset:
        val = pt[known_value]
        if val not in known_map:
            known_map[val] = list()
        known_map[val].append(pt)
        freq[val] = freq[val] + 1 if val in freq else 1
    return sum((freq[x] / len(dataset)) * entropy(known_map[x], header) for x in freq)


def best_factor(dataset: list, header: str):
    headers = list(key for key in dataset[0])
    headers.remove(header)
    vals = list([(expected_entropy(dataset, header, key), key) for key in headers])
    vals.sort(key=lambda k: k[0])
    return vals[0][1]


with open(sys.argv[1], mode='r') as csv_file:
    full_data = list(csv.DictReader(csv_file))

random.shuffle(full_data)
headers = list(iter(full_data[0]))
last_header = headers[-1]

NONMISSING = full_data
TEST = list(NONMISSING[i] for i in range(len(NONMISSING) - int(sys.argv[2]), len(NONMISSING)))
NOT_TEST = list(NONMISSING[i] for i in range(0, len(NONMISSING) - int(sys.argv[2])))
#
x = list([i for i in range(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))])
y = list()
for SIZE in range(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])):
    print(SIZE)
    TRAIN = random.sample(NOT_TEST, k=SIZE)
    while len(set([k[last_header] for k in TRAIN])) == 1:
        TRAIN = random.sample(NOT_TEST, k=SIZE)
    tree = Parent(TRAIN, [k for k in TRAIN[0]][-1])
    num = 0
    for item in TEST:
        if tree.get_expected_value(item) == item[last_header]:
            num += 1
    accuracy = num / len(TEST)
    y.append(accuracy)

plt.scatter(x, y)
plt.xlabel("Sample Size")
plt.ylabel("Accuracy")
plt.show()
