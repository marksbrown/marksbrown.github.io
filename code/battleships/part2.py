from string import ascii_uppercase
from random import random, choice


class Board:
    def __init__(self, N):
        assert 0 < N <= 26, "insufficient symbols!"
        self.N = N
        self.board = None
        self.empty()

    def empty(self):
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]

    def print(self, sep="  "):
        digits = len(str(self.N))

        print(" " * digits, *ascii_uppercase[: self.N], sep=sep)
        for j, row in enumerate(self.board, 1):
            print("{j:{digits}}".format(j=j, digits=digits), *row, sep=sep)

    def _check_horizontal(self, col, row, L):
        valid = 0 <= col <= self.N - L
        if not valid:
            return valid
        for j in range(col, col + L):
            if not self.board[row - 1][j]:
                valid = False

        return valid

    def _check_vertical(self, col, row, L):
        valid = 0 <= row <= self.N - L + 1

        if not valid:
            return valid
        for j in range(row, row + L):
            if not self.board[j - 1][col]:
                valid = False

        return valid

    def _attempt_to_place_ship(self, sym, row, L, horizontal=True):
        col = ascii_uppercase.index(sym)
        if horizontal and self._check_horizontal(col, row, L):
            for j in range(col, col + L):
                self.board[row - 1][j] = L
        elif not horizontal and self._check_vertical(col, row, L):
            for j in range(row - 1, row + L - 1):
                self.board[j][col] = L
        else:
            return False
        return True

    def randomly_place_ships(self, ships):
        assert sum(ships) <= self.N**2, "No overals allowed!"
        while ships:
            current_ship = ships.pop(0)
            r = False
            while not r:
                r = self._attempt_to_place_ship(
                    choice(ascii_uppercase[: self.N]),
                    choice(range(self.N)),
                    current_ship,
                    random() > 0.5,
                )
                
    def user_place_ships(self, ships):
        assert sum(ships) <= self.N**2, "No overals allowed!"
        while ships:
            current_ship = ships.pop(0)        
            while True:
                print(f"Place ship length of {current_ship}")
                sym = validated_input(f"Enter row ({ascii_uppercase[0]}-{ascii_uppercase[self.N - 1]}) >>", ascii_uppercase[:N], upperstr)
                col = validated_input(f"Enter col (0-{self.N}) >>", range(self.N), int)
                horizontal = validated_input(f"Horizontal (y/n) >>", 'yn', str)
                horizontal = horizontal.lower() == 'y'
                r = self._attempt_to_place_ship(
                    sym, col,
                    current_ship,
                    random() > 0.5,
                )
                if r:
                    break
                print("Invalid ship location, try again!")
                

def upperstr(v):
    if not v:
        raise ValueError()
    return str(v).upper()
        
def validated_input(prompt, options, dtype):
    while True:
        try:
            x = dtype(input(prompt))
        except ValueError:
            print("Invalid option, try again")
            continue
        if x in options:
            return x
        else:
            print("Invalid option, try again")
        

N = 5
first = Board(N)
r = first._attempt_to_place_ship('A', 1, 3)
print(r)
first.print()
ships = [3,4]
first.user_place_ships(ships)
first.print()
