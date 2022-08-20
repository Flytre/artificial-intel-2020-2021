import re

from colorama import init, Back, Style

init()


def highlight_matches(s, reg, flags=0):
    # Create match objects for every match of reg in s
    x = [match for match in re.finditer(reg, s, flags)]

    # Find the start and end indices of each match
    split_indices = []
    for match in x:
        split_indices.append((match.start(), match.end()))

    # Build a new string that inserts formatting before, and resets formatting after, each match
    pieces = []
    prev_end = 0
    for start, end in split_indices:
        pieces.append(s[prev_end:start])
        pieces.append(Back.LIGHTYELLOW_EX)
        pieces.append(s[start:end])
        pieces.append(Style.RESET_ALL)
        prev_end = end
    pieces.append(s[prev_end:])

    return ''.join(pieces)


# Set the text to be searched:
s = 'While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, ' \
    'into the ear of her friend,\n"Why indeed should I wind the clocks up, if they all run down in the end?" '

# Set the regular expression and any flags:
reg = "the.*?y"
flags = 0

# Print the results
print(highlight_matches(s, reg, flags))
