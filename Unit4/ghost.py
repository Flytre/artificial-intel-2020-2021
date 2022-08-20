import sys


class Dictionary:
    word_bank: set
    cache_children: dict
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    cache_descendants: dict

    def __init__(self, dictionary: str, min_len: int):
        with open(dictionary) as f:
            lines = [line.strip() for line in f]
            self.word_bank = set()
            for line in lines:
                if line.isalpha() and len(line) >= min_len:
                    self.word_bank.add(line.lower())
            self.cache_children = dict()
            self.cache_descendants = dict()

    def retrieve_child(self, word: str):
        if word not in self.cache_children:
            self.cache_children[word] = self.__find_children(word)
        return self.cache_children[word]

    def retrieve_descendants(self, word: str, possibles: set):
        if word not in self.cache_descendants:
            self.cache_descendants[word] = self.__find_descendants(word, possibles)
        return self.cache_descendants[word]

    def __find_children(self, word: str):
        children = set()
        for letter in Dictionary.alphabet:
            attempt = word + letter
            if attempt in self.word_bank:
                children.add(attempt)
        return children

    def __find_descendants(self, word: str, possibles: set):
        children = set()
        word_len = len(word)
        for entry in possibles:
            if len(entry) < word_len:
                continue
            if entry[0:word_len] == word:
                children.add(entry)
        return children

    def valid_letters(self, word, possibles: set):
        letters = set()
        word_len = len(word)

        for letter in Dictionary.alphabet:
            current = word + letter
            for entry in possibles:
                if len(entry) < word_len + 1:
                    continue
                if entry[0:word_len + 1] == current:
                    letters.add(letter)
                    break
        return letters


def player_move(word: str):
    word = word.lower()
    letters = list()
    possibles = dictionary.retrieve_descendants(word, dictionary.word_bank)
    if word in dictionary.word_bank:
        return "Already a word!"
    for letter in dictionary.valid_letters(word, possibles):
        attempt = word + letter
        if attempt in dictionary.word_bank:
            continue
        result = ai_step(attempt, dictionary.retrieve_descendants(attempt, possibles))
        if result is True:
            letters.append(letter.upper())
    if len(letters) > 0:
        letters.sort()
        return "Next player can guarantee victory by playing any of these letters: " + str(letters)
    return "Next player will lose!"


def player_step(word: str, possibles: set):
    for letter in dictionary.valid_letters(word, possibles):
        attempt = word + letter
        if attempt in dictionary.word_bank:
            continue
        result = ai_step(attempt, dictionary.retrieve_descendants(attempt, possibles))
        if result is True:
            return True
    return False


def ai_step(word: str, possibles: set):
    for letter in dictionary.valid_letters(word, possibles):
        attempt = word + letter
        if attempt in dictionary.word_bank:
            continue
        result = player_step(attempt, dictionary.retrieve_descendants(attempt, possibles))
        if result is False:
            return result
    return True


# SPECIFY ARGS HERE TO USE
args = sys.argv
dictionary = Dictionary(args[1], int(args[2]))

start = "" if len(args) < 4 else args[3]
print(player_move(start))
