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
    for i in range(len(parent)):
        for l in alphabet:
            if l == parent[i]:
                continue
            result = parent[:i] + l + parent[i + 1:]
            if result in lists:
                children.add(result)
    return children


def generate(start, end, lists, dicts):
    fringe = deque([])
    visited = set()
    fringe.append((start, [start]))
    visited.add(start)
    while len(fringe) > 0:
        f = fringe.popleft()
        if f[0] == end:
            return f[1]
        for i in get_children_or_place(f[0], lists, dicts):
            if not i in visited:
                newl = f[1].copy()
                newl.append(i)
                fringe.append((i, newl))
                visited.add(i)
    return None


with open("words_06_longer.txt") as f:
    lines = [line.strip() for line in f]
    words = {lines[0]}
    for line in lines:
        words.add(line)

start = time.perf_counter()
lists = create_list("words_06_longer.txt")
end = time.perf_counter()

print("Time to create the data structure was: " + str(end - start) + " seconds")
print("There are " + str(len(lists)) + " words in this dict.")
print()

start = time.perf_counter()
linenum = 0
dicts = dict()
with open('puzzles_longer.txt') as f:
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
