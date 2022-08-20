from collections import deque
# A = 2 length car, East-West
# B = 2 length car, North-South
# C = 3 length truck, East-West
# D = 3 length truck, North-South
# E = red car, always variant A

# . B . . . .
# . . . . B .
# E . B . . .
# . . . . . .
# B . . C . .
# . . . . . .

def is_in_bounds(x, y):
    return 0 <= x < 6 and 0 <= y < 6


class Vehicle:
    length = 0
    is_vertical = False
    x, y = 0, 0  # top left

    def __init__(self, length: int, vertical: bool, x: int, y: int):
        self.x, self.y = x, y
        self.length = length
        self.is_vertical = vertical

    def __str__(self):
        return self.str()

    def __repr__(self):
        return self.str()

    def str(self):
        return "x: {x}, y: {y} , len: {l}, dir: {d}".format(
            x=self.x,
            y=self.y,
            l=self.length,
            d=("vertical" if self.is_vertical else "horizontal")
        )

    def contains(self, x, y):
        """ does a vehicle contain a set of coordinates in its body """
        if self.is_vertical:
            return self.x == x and self.y <= y < self.y + self.length
        else:
            return self.y == y and self.x <= x < self.x + self.length

    def overlaps_vehicle(self, x, y, b):
        for v in b.vehicles:
            if self == v:
                continue
            if v.contains(x, y):
                return True
        return False

    def __eq__(self, other):

        if not isinstance(other, Vehicle):
            return False

        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y, self.length, self.is_vertical))

    def can_move_to(self, new_x, new_y, b) -> bool:
        """ checks if the position is a valid position for the car, without checking whether or not it can actually get there. """
        if self.is_vertical:
            for y in range(new_y, new_y + self.length):
                if self.overlaps_vehicle(new_x, y, b) or not is_in_bounds(new_x, y):
                    return False
            return True
        else:
            for x in range(new_x, new_x + self.length):
                if self.overlaps_vehicle(x, new_y, b) or not is_in_bounds(x, new_y):
                    return False
            return True


    def children(self, b) -> list:
        children = list()
        if not self.is_vertical:
            for i in range(self.x + 1, 6):
                if self.can_move_to(i, self.y, b):
                    children.append(Vehicle(self.length, self.is_vertical, i, self.y))
                else:
                    break
            for i in range(self.x - 1, -1, -1):
                if self.can_move_to(i, self.y, b):
                    children.append(Vehicle(self.length, self.is_vertical, i, self.y))
                else:
                    break
        else:
            for i in range(self.y + 1, 6):
                if self.can_move_to(self.x, i, b):
                    children.append(Vehicle(self.length, self.is_vertical, self.x, i))
                else:
                    break
            for i in range(self.y - 1, -1, -1):
                if self.can_move_to(self.x, i, b):
                    children.append(Vehicle(self.length, self.is_vertical, self.x, i))
                else:
                    break
        return children


class Board:
    vehicles = frozenset()
    red: Vehicle
    parent = None

    def __init__(self, red: Vehicle, vehicles: frozenset, parent=None):
        self.red = red
        self.vehicles = vehicles
        self.parent = parent

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return self.vehicles == other.vehicles and self.red == other.red

    def __hash__(self):
        return hash((self.red,tuple(self.vehicles)))

    def __str__(self):
        ret = ""
        for v in self.vehicles:
            ret += v.__str__() + "\n"
        ret += "Red: "+self.red.__str__()
        return ret

    def __repr__(self):
        return self.__str__()

    def get_children(self):
        boards = list()
        for vehicle in self.vehicles:
            vchildren: list = vehicle.cache_children(self)

            for vchild in vchildren:
                copy: set = self.vehicles.copy()
                copy.remove(vehicle)
                copy.add(vchild)
                if vehicle == self.red:
                    boards.append(Board(vchild, copy, self))
                else:
                    boards.append(Board(self.red, copy, self))
        return boards


    def is_goal(self):
        for i in range(self.red.x + 1, 5):
            if self.red.can_move_to(i, self.red.y, self):
                continue
            else:
                return False
        return True



def createInitialBoard(file: str):
    red: Vehicle
    vehicles = set()
    with open(file) as f:
        for row, line in enumerate(f):
            for col, ch in enumerate(line):
                if not ch in {"A", "B", "C", "D", "E"}:
                    continue

                length = 2
                is_vertical = False
                if ch == "A" or ch == "E":
                    length = 2
                    is_vertical = False
                elif ch == "B":
                    length = 2
                    is_vertical = True
                elif ch == "C":
                    length = 3
                    is_vertical = False
                elif ch == "D":
                    length = 3
                    is_vertical = True
                if ch == "E":
                    red = Vehicle(length, is_vertical, col // 2, row)
                    vehicles.add(red)
                else:
                    vehicles.add(Vehicle(length, is_vertical, col // 2, row))
    return Board(red,vehicles)


def bfs(start: Board):
    to_visit = deque()
    visited = {start}
    to_visit.append(start)
    goal: Board = None

    while len(to_visit) > 0:
        curr: Board = to_visit.popleft()
        if curr.is_goal():
            goal = curr
            break
        children = curr.get_children()
        for child in children:
            if child not in visited:
                to_visit.append(child)
                visited.add(child)

    states = list()
    temp = goal
    length = 0
    while temp != None:
        states.append(temp)
        temp = temp.parent
        length += 1
    return length, list(reversed(states))


board = createInitialBoard("puzzle_eckel.txt")
length, path = bfs(board)

print(path)

print("length = ", length)

