import sys


def int_to_bin(n: int, length: int):
    return tuple([int(ch) for ch in
                  '{message:{fill}{align}{width}}'.format(
                      message=str(bin(n))[2:],
                      fill='0',
                      align='>',
                      width=length,
                  )
                  ])


def truth_table(bits, n):
    outs = tuple(reversed(int_to_bin(n, 2 ** bits)))
    res = dict({int_to_bin(i, bits): outs[i] for i in range(0, 2 ** bits)})
    return res


def pretty_print_table(table):
    v = len(([k for k in table.keys()][0]))
    print(" ".join(list([str(i + 1) for i in range(0, v)])), "| O")
    print((3 + 2 * v) * "-")
    for key in reversed(sorted(table.keys())):
        print(" ".join([str(i) for i in key]), "|", table[key])


def perceptron(activation, weight: tuple, bias: float, x: tuple):
    return activation(sum([i * j for (i, j) in zip(weight, x)]) + bias)


def check(n: int, weight: tuple, bias: float):
    table = truth_table(len(weight), n)
    return len([k for k in table if perceptron(lambda t: 1 if t > 0 else 0, weight, bias, k) == table[k]]) / len(
        table.keys())


def train(n: int, table: truth_table, weight: tuple, bias: float, activation):
    last_weight = weight
    gens = 0
    while gens < 100:
        for key in reversed(list(table.keys())):
            f_star = perceptron(activation, weight, bias, key)
            weight = tuple(val + (table[key] - f_star) * key[index] for index, val in enumerate(weight))
            bias = bias + (table[key] - f_star)
        if weight == last_weight and check(n, weight, bias) == 1.0:
            return weight, bias
        else:
            last_weight = weight
            gens += 1
    return weight, bias


def lab(bits: int):
    correct = 0
    for n in range(0, 2 ** 2 ** bits):
        table = truth_table(bits, n)
        result = train(n, table, (0,) * bits, 0, lambda t: 1 if t > 0 else 0)
        print("result for", n, ":", result[0], result[1], check(n, result[0], result[1]))
        if check(n, result[0], result[1]) == 1.0:
            correct += 1
    print(2 ** 2 ** bits, "possible functions;", correct, "can be correctly modeled.")


bt = int(sys.argv[1])
can = int(sys.argv[2])
res = train(can, truth_table(bt, can), (0,) * bt, 0, lambda t: 1 if t > 0 else 0)
print("result for", can, ": weight=", res[0], "bias=", res[1], "accuracy=", check(can, res[0], res[1]))
