import sys
from collections import deque
import time


def create_list(f):
    with open(f) as file:
        words = set()
        for line in file:
            w = line.strip()
            words.add(w)
        return words


def get_children_or_place(parent, lists, dicts):
    if parent not in dicts:
        dicts[parent] = get_children(parent, lists)
    return dicts[parent]


def get_children(parent, lists):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    children = set()
    for index in range(0, len(parent)):
        start_of = parent[:index]
        end_of = parent[index + 1:]
        for letter in alphabet:
            if letter == parent[index]:
                continue
            result = start_of + letter + end_of
            if result in lists:
                children.add(result)
    return children


def generate(start, end, lists, dicts):
    fringe = deque()
    visited = set()
    fringe.append((start, None))
    visited.add(start)
    while len(fringe) > 0:
        f = fringe.popleft()
        if f[0] == end:
            l = [f[0]]
            curr = f[1]
            while curr is not None:
                l.insert(0, curr[0])
                curr = curr[1]
            return l
        for i in get_children_or_place(f[0], lists, dicts):
            if not i in visited:
                fringe.append((i, f))
                visited.add(i)
    return None


start = time.perf_counter()
lists = create_list("words_06_longer.txt")
end = time.perf_counter()

print("Time to create the data structure was: " + str(end - start) + " seconds")
print("There are " + str(len(lists)) + " words in this dict.")
print()

start = time.perf_counter()
linenum = 0
dicts = dict()
with open("puzzles_longer.txt") as f:
    for line in f:
        print("Line: " + str(linenum))
        a = line.split()
        l = generate(a[0], a[1], lists, dicts)
        if l == None:
            print("No solution!")
            print()
            linenum += 1
            continue
        print("Length is: " + str(len(l)))
        for i in l:
            print(i)
        print()
        linenum += 1
end = time.perf_counter()
print("Time to solve all of the puzzles was: " + str(end - start) + " seconds")
