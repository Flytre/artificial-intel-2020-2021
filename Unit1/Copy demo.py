import time, copy

# Instructions are at the bottom!

def demo1():
    a = [1, 2, 3]
    b = a
    b[0] = 4
    print(a)
    print(b)
    print()

    a = [1, 2, 3]
    b = a.copy()
    b[0] = 4
    print(a)
    print(b)
    print()

    a = [[1, 2], [3, 4], [5, 6]]
    b = a.copy()
    a[0][0] = 4
    print(a)
    print(b)
    print()


def demo2():
    a = [[1, 2], [3, 4], [5, 6]]
    b = copy.deepcopy(a)
    a[0][0] = 4
    print(a)
    print(b)
    print()

    a = [[1, 2], [3, 4], [5, 6]]
    b = [l.copy() for l in a]
    a[0][0] = 4
    print(a)
    print(b)
    print()

def demo3():
    # This will make a 1000x1000 2D array
    a = [[x for x in range(1000)] for y in range(1000)]

    start = time.perf_counter()
    print("Performing list comprehension copy number ", end = '')
    for count in range(100):
        print(count, "", end = '')
        b = [l.copy() for l in a]
    end = time.perf_counter()
    print()
    print("100 comprehension copies took", end-start, "seconds")
    print()

    start = time.perf_counter()
    print("Performing deepcopy copy number ", end='')
    for count in range(100):
        print(count, "", end='')
        b = copy.deepcopy(a)
    end = time.perf_counter()
    print()
    print("100 deepcopy copies took", end - start)
    print()


# Run demo 1.  Analyze the output and answer the questions on the website.
# Then, comment demo 1 and uncomment demo 2, run that, and answer those questions.
# Finally, the same for demo 3.
# Only run and discuss one demo at a time!

# demo1()
# demo2()
# demo3()