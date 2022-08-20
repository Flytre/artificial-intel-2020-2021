import csv
import math
import sys


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
        for pt in data:
            val = pt[self.factor]
            if val not in split_data:
                split_data[val] = list()
            split_data[val].append(pt)
        for key in split_data:
            if entropy(split_data[key], header) == 0:
                self.nodes[key] = Leaf(split_data[key], header)
            else:
                self.nodes[key] = Parent(split_data[key], header)

    def print(self):
        print(recursive_print(0, self))

    def __str__(self):
        return recursive_print(0, self)


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


with open("mushroom.csv", mode='r') as csv_file:
    full_data = list(csv.DictReader(csv_file))
out_file = open("treeout.txt", "wt")
out_file.write(Parent(full_data, [k for k in full_data[0]][-1]).__str__())
out_file.close()
