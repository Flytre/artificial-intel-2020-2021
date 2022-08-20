def readable(val: str):
    if len(val) == 0:
        return set()
    if len(val) == 1:
        return set(val)
    result = set()
    for index, character in enumerate(val):
        val_excluding_character = val[0:index] + val[index + 1:len(val)]
        permutations_excluding_character = readable(val_excluding_character)
        for permutation in permutations_excluding_character:
            result.add(character + permutation)
    return result


def elegant(val: str):
    if len(val) <= 1:
        return set(val)
    result = set()
    for i, ch in enumerate(val):
        result = result.union(set(ch + l for l in elegant(val[0:i] + val[i + 1:len(val)])))
    return result


def very_elegant(val: str):
    return set(val) if len(val) <= 1 else set(
        ch + l for i, ch in enumerate(val) for l in very_elegant(val[0:i] + val[i + 1:len(val)]))


print(very_elegant("abcd"))
