import math
import sys

args: list = sys.argv

# print sum of next 3 ints
if args[1] == "A":
    print(sum(int(args[i]) for i in range(2, 5)))

# print sum of all ints following
elif args[1] == "B":
    print(sum(int(args[i]) for i in range(2, len(args))))

# print list of all args divisible by 3
elif args[1] == "C":
    ints = []
    for i in range(2, len(args)):
        if int(args[i]) % 3 == 0:
            ints.append(int(args[i]))
    print(ints)

# print first X fibonacci numbers
elif args[1] == "D":
    fib = [1, 1]
    for i in range(1, int(args[2]) - 1):
        fib.append(fib[i] + fib[i - 1])
    print(fib)

# print the value of f(k) = k^2 − 3k + 2 for each integer between the two inputs (eg, 2 5 = 0, 2, 6, 12).
elif args[1] == "E":
    results = list(pow(i, 2) - 3 * i + 2 for i in range(int(args[2]), int(args[3]) + 1))
    print(results)

# given 3 floats, print the area of the triangle formed by these side lengths
elif args[1] == "F":
    p = sum(float(args[i]) for i in range(2, 5)) / 2
    filler = p * (p - float(args[2])) * (p - float(args[3])) * (p - float(args[4]))
    if filler < 0:
        print("Invalid Triangle")
    else:
        print(math.sqrt(filler))

# print the count of each vowel in a string
elif args[1] == "G":
    vowels = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for c in args[2].lower():
        for vowel in vowels:
            if c == vowel:
                vowels[vowel] += 1
    print(vowels)
