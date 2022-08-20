import sys

args: list = sys.argv

string = args[1]

# if you read this expect the comments to get a lot more lax in the future hahaha

print("#1:", string[2])  # position 2
print("#2:", string[4])  # fifth character
print("#3:", len(string))  # the length
print("#4:", string[0])  # first character
print("#5:", string[-1])  # last character
print("#6:", string[-2])  # penultimate character
print("#7:", string[3:8])  # five character long substring from pos 3
print("#8:", string[-5:])  # las1t five characters
print("#9:", string[2:])  # third character onward
print("#10:", string[::2])  # every other character
print("#11:", string[1::3])  # every third character from 2nd
print("#12:", string[::-1])  # reversed
print("#13:", string.find(" "))  # index of space
print("#14:", string[:-1])  # last character removed
print("#15:", string[1:])  # first character removed
print("#16:", string.lower())  # lowercase
print("#17:", string.split())  # delimit by whitespace
print("#18:", len(string.split()))  # number of space delimited words
print("#19:", list(string))  # char list

print("#20:", "".join(sorted(string)))  # create new string and make it a sorted version of the original string.

print("#21:", string.split(" ")[0])  # a new string containing up to but not including the 1st space

print("#22:", string == string[::-1])  # palindrome check
