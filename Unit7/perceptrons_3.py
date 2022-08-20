import sys
import ast


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


def step(t: int):
    return 1 if t > 0 else 0


# XOR HAPPENS HERE
def xor(in1: int, in2: int):
    return perceptron(step, (-1, -1), 0.5,  # NOR
                      (perceptron(step, (1, 1), -1.5, (in1, in2)),  # AND
                       perceptron(step, (-1, -1), 0.5, (in1, in2))))  # NOR


ins = ast.literal_eval(sys.argv[1])
print(xor(ins[0], ins[1]))
