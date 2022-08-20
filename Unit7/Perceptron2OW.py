import sys
import ast
import matplotlib.pyplot as plt

def possible(bits, s = ""):
    if len(s) == bits:
        return s
    else:
        holder = possible(bits, s + "1") + "\n"
        holder += possible(bits, s + "0")
        return holder

def truth_table(bits, n):
    h = 2 ** bits
    o = bin(n)
    o = o[2:]
    for i in range(h - len(o)): 
        o = "0" + o
    #holder = ''
    '''for x in range(h - len(o)): 
        holder += '0'
    o = holder + o'''
    holder = possible(bits)
    r = ()
    final = ()
    index = 0
    for i in holder:
        if i == "1" or i == "0": 
            r = r + (int(i),)
        else: 
            final = final + (((r), int(o[index: index + 1])),)
            index += 1
            r = ()
    final = final + (((r), int(o[index: index + 1])),)
    return final

def print_table(table, bits):
    printing = ""
    printing2 = ""
    for x in range(bits): 
        printing += "In" + str(x) + "   "
        printing2 += "-------"
    print(printing + "|   Out")
    print(printing2 + "------")
    for r in table:
        printrow = ""
        value = r[0]
        for i in value: 
            printrow += " " + str(i) + "    "
        print(printrow + "|    " + str(r[1]))
    
def step(num):
    if num > 0: 
        return 1
    else: 
        return 0

def perceptron(A, w, b, x):
    dot = 0
    for i in range(len(w)): 
        dot += w[i] * x[i]
    return A(dot + b)

def check(n, w, b):
    correct = 0
    table = truth_table(len(w), n)
    for r in table:
        i = r[0]
        o = r[1]
        if perceptron(step, w, b, i) == o: 
            correct += 1
    return correct/len(table)

def check2(table, w, b):
    correct = 0
    for r in table:
        i = r[0]
        o = r[1]
        if perceptron(step, w, b, i) == o: 
            correct += 1
    return correct/len(table)

def outs(bits):
    return [i for i in range(2 ** (2 ** bits))]

def weight(w, x, d):
    holder = []
    output = []
    for i in range(len(x)):
        holder.append(x[i] * d)
    for i in range(len(w)):
        output.append(w[i] + holder[i])
    return tuple(output)

def train(table, w, b):
    prevw = None
    prevb = None
    epoch = 0
    while not (prevw == w and prevb == b) and epoch <= 100:
        #print(epoch)
        prevw = w
        prevb = b
        epoch += 1
        for r in table:
            i = r[0]
            o = r[1]
            fstar = perceptron(step, w, b, i)
            w = weight(w, i, o - fstar)
            b += o - fstar
    return (w, b)


def model(bits):
    total = outs(bits)
    correct = 0
    for i in total:
        #print(i)
        currtable = truth_table(bits, i)
        w_b = train(currtable, tuple([0 for b in range(bits)]), 0)
        percent = check2(currtable, w_b[0], w_b[1])
        if percent == 1:
            correct += 1
    print(str(len(total)) + " possible functions; " + str(correct) + " can be correctly modeled.")

def graph():
    numgraph = outs(2)
    x = [i/10 for i in range(-20, 21)]
    y = [i/10 for i in range(-20, 21)]
    for i in numgraph:
        plt.figure(i)
        axes = plt.gca()
        axes.set_xlim([-2, 2])
        axes.set_ylim([-2, 2])
        #plt.xlim([-2, 2])
        #plt.ylim([-2, 2])
        color = []
        sizes = []
        plotx = []
        ploty = []
        largedotxg = []
        largedotyg = []
        largedotxr = []
        largedotyr = []
        currtable = truth_table(2, i)
        for r in currtable:
            i = r[0]
            o = r[1]
            if o == 1:
                largedotxg.append(i[0])
                largedotyg.append(i[1])
            else:
                largedotxr.append(i[0])
                largedotyr.append(i[1])
        w_b = train(currtable, (0, 0), 0)
        for j in x:
            for z in y:
                if not ((j == 0 or j == 1) and (z == 0 or z == 1)):
                    plotx.append(j)
                    ploty.append(z)
                    sizes.append(10)
                    p = perceptron(step, w_b[0], w_b[1], (j, z))
                    if p == 1:
                        color.append("green")
                    else:
                        color.append("red")
        for q in range(len(largedotxg)):
            plotx.append(largedotxg[q])
            ploty.append(largedotyg[q])
            sizes.append(30)
            color.append("green")
        for q in range(len(largedotxr)):
            plotx.append(largedotxr[q])
            ploty.append(largedotyr[q])
            sizes.append(30)
            color.append("red")
        plt.scatter(plotx, ploty, s = sizes, c = color)
        plt.show()


#bits = int(sys.argv[1])
#n = int(sys.argv[2])
#print_table(truth_table(bits, n), bits)
#print(perceptron(step, (1,1),-1.5, (1,0)))
#print(check(50101, (3,2,3,1), -4))
'''n = int(sys.argv[1])
x = sys.argv[2]
w = ast.literal_eval(x)
b = float(sys.argv[3])
print(check(n, w, b))'''
#print(outs(2))
#model(4)
'''t = truth_table(3, 73)
print(t)
wb = train(t, (0, 0, 0), 0)'''
'''bit = int(sys.argv[1])
canonical = int(sys.argv[2])
table = truth_table(bit, canonical)
w_b = train(table, tuple([0 for b in range(bit)]), 0)
percent = check2(table, w_b[0], w_b[1])
print("Final weight vector: " + str(w_b[0]))
print("Final bias value: " + str(w_b[1]))
print("Accuracy of perceptron: " + str(percent))'''
graph()
'''x = [i/10 for i in range(-20, 21)]
print(x)'''
