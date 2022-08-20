import sys


# left child of root
def left(i):
    return 2 * i + 1


# right child of root
def right(i):
    return 2 * (i + 1)


# parent of a node
def parent(i):
    return (i - 1) // 2


# whether the left child exists
def exist_left(i):
    return len(heap) > left(i)


# whether the right child exists
def exist_right(i):
    return len(heap) > right(i)


# whether the node is a leaf node
def leaf(i):
    return not exist_left(i) and not exist_right(i)


# tests if the heap is in min-heap order: debugging, not used in any method
def in_order(i):
    if i >= len(heap) or leaf(i):
        return True
    if exist_left(i) and not exist_right(i):
        return heap[i] <= heap[left(i)] and in_order(left(i))
    if exist_right(i) and not exist_left(i):
        return heap[i] <= heap[right(i)] and in_order(right(i))
    else:
        return heap[i] <= heap[left(i)] and heap[i] <= heap[right(i)] and in_order(left(i)) and in_order(right(i))


# gets the minimum value from the root: checks 4 cases based on whether its a leaf, single parent on each side or has
# both children. Recursively finds the minimum of each the children's heaps then compares those values.
def min(root):
    if leaf(root):
        return root
    if exist_left(root) and not exist_right(root):
        m = min(left(root))
        return m if heap[m] < heap[root] else root
    if exist_right(root) and not exist_left(root):
        m = min(right(root))
        return m if heap[m] < heap[root] else root
    if exist_right(root) and exist_left(root):
        # if it has 2 children return the index containing the minimum of the
        # node and the minimum of each of its children

        min_left_side = min(left(root))  # min of left child
        min_right_side = min(right(root))  # min of right child
        if heap[min_left_side] <= heap[min_right_side] and heap[min_left_side] < heap[root]:
            return min_left_side
        if heap[min_right_side] <= heap[min_left_side] and heap[min_right_side] < heap[root]:
            return min_right_side
        return root
    return root  # if this runs that means something went terribly wrong but whatever


# starts at the root and sets it to the minimum value in the heap. Then it works down and sets each node's value to
# the minimum of its own sub-heap.

def heapify():
    for i in range(0, len(heap)):
        m = min(i)
        if heap[m] < heap[i]:
            heap[m], heap[i] = heap[i], heap[m]


# Adds the new item to the end, then swaps it with its parent until heap rules are preserved O(log(n))

def heappush(val):
    i = len(heap)  # index of appended item
    heap.append(val)  # add the value to the end
    while i > 0 and heap[i] < heap[parent(i)]:  # move the value higher up the tree until it is in the right place
        heap[parent(i)], heap[i] = heap[i], heap[parent(i)]
        i = max(parent(i), 0)


# swaps the 1st element, with the last one, pops it off, and shifts the new 1st element down until its in the right
# place O(log(n))

def heappop():
    heap[0], heap[-1] = heap[-1], heap[0]
    min_val = heap.pop()
    i = 0  # index of what was previous the last node

    # Not very easy on the eyes, but effectively just swaps the node with its children if its larger than them until
    # heap order is preserved
    while not leaf(i):
        if exist_right(i) and not exist_left(i):
            if heap[right(i)] < heap[i]:
                heap[right(i)], heap[i] = heap[i], heap[right(i)]
                i = right(i)
            else:
                break
        elif exist_left(i) and not exist_right(i):
            if heap[left(i)] < heap[i]:
                heap[left(i)], heap[i] = heap[i], heap[left(i)]
                i = left(i)
            else:
                break
        else:
            if heap[left(i)] <= heap[right(i)] and heap[left(i)] < heap[i]:
                heap[left(i)], heap[i] = heap[i], heap[left(i)]
                i = left(i)
            elif heap[right(i)] <= heap[left(i)] and heap[right(i)] < heap[i]:
                heap[right(i)], heap[i] = heap[i], heap[right(i)]
                i = right(i)
            else:
                break
    return min_val


# Main code:

# if it only has a file name there's nothing to do, so quit
if len(sys.argv) < 2:
    quit()

# figure out when the flood of initial numbers ends, and set that part of sys.argv to contain the heap
index = next((i for i, x in enumerate(sys.argv[1:]) if x == 'A' or x == 'R'), -1)
heap = list(int(i) for i in sys.argv[1: index + 1]) if index != -1 else []
print("Initial List:", heap)

# heapify and print
heapify()
print("Heapified List:", heap)

# Process each value and print the operation
for i in range(index + 1, len(sys.argv)):
    if sys.argv[i] == 'A':
        heappush(int(sys.argv[i + 1]))
        print("Added " + sys.argv[i + 1] + " to heap:", heap)
    elif sys.argv[i] == 'R':
        print("Popped", heappop(), "from heap:", heap)
    else:
        continue
