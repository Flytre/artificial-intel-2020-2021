import random
import sys
from string import ascii_uppercase
from math import log

# Constants
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8
FREQUENCY_BASE = 2

gram_freq = {line[0]: log(int(line[1]), FREQUENCY_BASE) for line in
             [line.strip().split(" ") for line in open(file="ngrams.txt")]}
alpha_dict = {char: index for (index, char) in enumerate(ascii_uppercase)}


def encode_char(char: str, cipher: str):
    return cipher[alpha_dict[char]] if char.isalpha() else char


def encode(message: str, cipher: str):
    return "".join(([encode_char(char, cipher) for char in message.upper()]))


def decode_char(char: str, cipher: str):
    return ascii_uppercase[cipher.index(char)] if char.isalpha() else char


def decode(message: str, cipher: str):
    return "".join(([decode_char(char, cipher) for char in message.upper()]))


def n_grams(message: str, n: int):
    return list([message[i:i + n] for i in range(0, len(message) - n + 1)])


fitness_cache = dict()


def fitness(message: str, cipher: str, n: int):
    return sum([gram_freq[n_gram] for n_gram in n_grams(decode(message, cipher).strip(), n) if
                n_gram in gram_freq.keys()])


def rand_permutation():
    return "".join(sorted([i for i in ascii_uppercase], key=lambda k: random.random()))


def rand_permutations(n: int):
    curr = set([rand_permutation() for i in range(0, n)])
    while len(curr) < n:
        curr.add(rand_permutation())
    return curr


def replace_char(string: str, index: int, new: str):
    return string[0:index] + new + string[index + 1:]


def breed(cipher1: str, cipher2: str):
    result = [""] * len(cipher1)
    added = set()
    indices = random.sample(range(len(cipher1)), CROSSOVER_LOCATIONS)
    for index in indices:
        result[index] = cipher1[index]
        added.add(cipher1[index])
    current_index = 0
    for char in cipher2:
        if char not in added:
            while len(result[current_index]) != 0:
                current_index += 1
            result[current_index] = char
    return "".join(result)


def breed_alt(cipher1: str, cipher2: str):
    result = [""] * len(cipher1)
    added = set()
    indices = random.sample(range(len(cipher1)), 12)
    for index in indices:
        result[index] = cipher1[index]
        added.add(cipher1[index])
    indices = random.sample(range(len(cipher2)), 14)
    for index in indices:
        if cipher2[index] not in added:
            if result[index] in added:
                added.remove(result[index])
            result[index] = cipher2[index]
            added.add(cipher2[index])
    current_index = 0
    for char in cipher2:
        if char not in added:
            while len(result[current_index]) != 0:
                current_index += 1
            result[current_index] = char
    return "".join(result)


def swap_random(cipher: str):
    i1, i2 = random.sample(range(len(cipher)), 2)
    c1, c2 = cipher[i1], cipher[i2]
    return replace_char(replace_char(cipher, i1, c2), i2, c1)


def hill_climb(message: str):
    cipher = rand_permutation()
    mx = fitness(message, cipher, 4)
    unchanging = 0
    while unchanging < 2500:
        attempt = swap_random(cipher)
        fit = fitness(message, attempt, 4)
        if fit > mx:
            mx = fit
            cipher = attempt
            unchanging = 0
            print(decode(message, cipher))
        else:
            unchanging += 1
    return decode(message, cipher)


def next_generation(current_generation: list, message: str, n: int):
    next_gen = set()
    ranked = current_generation  ## removed .copy()
    fitness_dict = dict()
    for key in current_generation:
        fitness_dict[key] = fitness(message, key, n)
    ranked.sort(key=lambda val: fitness_dict[val], reverse=True)
    print(decode(message, ranked[0]), fitness_dict[ranked[0]])
    copied_clones = 0
    while copied_clones < NUM_CLONES and copied_clones < len(current_generation):
        next_gen.add(ranked[copied_clones])
        copied_clones += 1
    while len(next_gen) < POPULATION_SIZE:
        child = tournament(current_generation, message, n, fitness_dict)
        if random.random() < MUTATION_RATE:
            child = swap_random(child)
        next_gen.add(child)
    return list(next_gen)


def tournament(current_generation: list, message: str, n: int, fitness_dict: dict):
    competitor_indices = random.sample(current_generation, TOURNAMENT_SIZE * 2)
    alpha = list([competitor_indices[i] for i in range(0, TOURNAMENT_SIZE)])
    beta = list(competitor_indices[i] for i in range(TOURNAMENT_SIZE, 2 * TOURNAMENT_SIZE))
    p1, p2 = tournament_parent_finder(alpha, message, n, fitness_dict), tournament_parent_finder(beta, message, n,
                                                                                                 fitness_dict)
    return breed_alt(p1, p2)


def tournament_parent_finder(competitors: list, message: str, n: int, fitness_dict: dict):
    competitors.sort(key=lambda val: fitness_dict[val], reverse=True)
    parent, index = None, 0
    while parent is None:
        if random.random() < TOURNAMENT_WIN_PROBABILITY:
            parent = competitors[index]
        else:
            index += 1
    return parent if parent is not None else competitors[TOURNAMENT_SIZE - 1]


msg = sys.argv[1]

current_gen = list(rand_permutations(POPULATION_SIZE))
value = next_generation(current_gen, msg, 4)

for i in range(0, 499):
    value = next_generation(value, msg, 3 if random.random() < 0.5 else 4)
