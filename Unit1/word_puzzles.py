from collections import deque
import time
import sys


class WordLadder:
    word = ""
    parent = None

    def __init__(self, word, parent):
        self.word = word
        self.parent = parent

    def __eq__(self, obj):
        return isinstance(obj, WordLadder) and obj.word == self.word

    def __hash__(self):
        return hash(self.word)

    def get_parent(self):
        return self.parent

    def get_content(self):
        return self.word

    def __str__(self):
        return self.word

    def get_path(self):
        path = deque()
        path.append(self.word)
        parent = self.parent
        while parent is not None:
            path.append(parent.word)
            parent = parent.parent
        return path


def create_dictionary(dictionary):
    with open(dictionary) as f:
        lines = [line.strip() for line in f]
        words = {lines[0]}
        for line in lines:
            words.add(line)
        return words


hashed = dict()


def get_children_or_hash(parent: str, dictionary: set):
    if parent not in hashed:
        hashed[parent] = get_children(parent, dictionary)
    return hashed[parent]


def get_children(parent: str, dictionary: set):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    children = set()
    for index in range(0, len(parent)):
        start_of = parent[:index]
        end_of = parent[index + 1:]
        for letter in alphabet:
            if letter == parent[index]:
                continue
            result = start_of + letter + end_of
            if result in dictionary:
                children.add(result)
    return children


def make_ladder(start: str, end: str):
    to_visit = deque()
    visited: set = {start}
    to_visit.append((start, None))
    goal = None

    while len(to_visit) > 0:
        curr = to_visit.popleft()
        if curr[0] == end:
            goal = curr
            break
        children = get_children_or_hash(curr[0], d)
        for child in children:
            if child not in visited:
                to_visit.append((child, curr))
                visited.add(child)
    return goal


def singletons(dictionary: set):
    c = 0
    for word in dictionary:
        children = get_children(word, dictionary)
        if len(children) == 0:
            c += 1
    return c


def longest_chain_from_word(start: str, dictionary: set):
    to_visit = deque()
    visited: set = {WordLadder(start, None)}
    to_visit.append(WordLadder(start, None))

    while len(to_visit) > 0:
        curr = to_visit.popleft()
        children = get_children(curr.word, dictionary)
        for child in children:
            if WordLadder(child, curr) not in visited:
                to_visit.append(WordLadder(child, curr))
                visited.add(WordLadder(child, curr))
    maxi = 0
    max_word = WordLadder("", None)
    for combo in visited:
        length = 0
        combo2 = combo
        while combo2.get_parent() is not None:
            combo2 = combo2.get_parent()
            length += 1
        if length > maxi:
            maxi = length
            max_word = combo

    path = list()
    while max_word is not None:
        path.append(max_word.get_content())
        max_word = max_word.get_parent()

    return path


def longest_chain(dictionary: set):
    word_paths = dict()
    for word in dictionary:

        children = get_children(word, dictionary)
        if len(children) == 0:
            continue
        word_paths[word] = longest_chain_from_word(word, dictionary)

    longest_path = 0
    longest_word = ""
    for key in word_paths:
        le = len(word_paths[key])
        if le > longest_path:
            longest_word = key
            longest_path = le
    return word_paths[longest_word]


# returns size of the clump
# removes all words in the clump from the dictionary of words
def clump(start: str, dictionary: set):
    to_visit = deque()
    visited: set = {WordLadder(start, None)}
    to_visit.append(WordLadder(start, None))

    while len(to_visit) > 0:
        curr = to_visit.popleft()
        children = get_children(curr.word, dictionary)
        for child in children:
            if WordLadder(child, curr) not in visited:
                to_visit.append(WordLadder(child, curr))
                visited.add(WordLadder(child, curr))
    for word in visited:
        if word.get_board() in dictionary:
            dictionary.remove(word.get_board())
    return len(visited)


def clump_organization(dictionary: set):
    dictionary_clone = set()
    for word in dictionary:
        children = get_children(word, dictionary)
        if len(children) > 0:
            dictionary_clone.add(word)

    max_clump_size = 0
    num_clumps = 0
    while len(dictionary_clone) > 0:
        item = clump(dictionary_clone.pop(), dictionary_clone)
        num_clumps += 1
        if item > max_clump_size:
            max_clump_size = item
    print("Max size:", max_clump_size)
    print("Num Clumps:", num_clumps)


start = time.perf_counter()
d = create_dictionary("words_06_longer.txt")
end = time.perf_counter()
print("Time to create the data structure was:", (end - start), "seconds")
print("There are", len(d), "words in the dict.")
total_time = 0
with open("puzzles_longer.txt") as f:
    current_line = 0
    for line in f:
        print("")
        print("Line", current_line)
        current_line += 1
        start = line.split()[1]
        end = line.split()[0]

        path = list()
        start2 = time.perf_counter()
        ladder = make_ladder(start, end)
        end2 = time.perf_counter()
        total_time += (end2 - start2)
        while ladder is not None:
            path.append(ladder[0])
            ladder = ladder[1]
        if len(path) > 0:
            print("Length is:", len(path))
            for word in path:
                print(word)
        else:
            print("No solution!")
print("Time to solve all of these puzzles was:", total_time, "seconds")
