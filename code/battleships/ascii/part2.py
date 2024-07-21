"""
Part 2

Rewriting with classes and functions
added ship placement
"""

from string import ascii_uppercase
from random import random, choice, randint, shuffle


def as_row(v: int) -> int:
    if v <= 0:
        raise ValueError(f"{v} is somehow negative or zero?!")
    return v - 1


def as_col(v: str) -> int:
    return ascii_uppercase.index(v)


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
        valid = 0 <= col < self.N - L
        if not valid:
            return valid
        for j in range(col, col + L):
            if self.board[row][j]:
                valid = False

        return valid

    def _check_vertical(self, col, row, L):
        valid = 0 <= row <= self.N - L

        if not valid:
            return valid
        for j in range(row, row + L):
            if self.board[j][col]:
                valid = False

        return valid

    def _attempt_to_place_ship(self, sym, row, L, horizontal=True):
        col = as_col(sym)
        row = as_row(row)
        if horizontal and self._check_horizontal(col, row, L):
            for j in range(col, col + L):
                self.board[row][j] = L
        elif not horizontal and self._check_vertical(col, row, L):
            for j in range(row, row + L):
                self.board[j][col] = L
        else:
            return False
        return True

    def place_ships(self):
        pass


class ComputerBoard(Board):
    def __init__(self, N, ships):
        super().__init__(N)
        self.place_ships(ships)

    def place_ships(self, ships, max_attempts=50):
        assert sum(ships) <= self.N**2, "No overals allowed!"
        while ships:
            current_ship = ships.pop(0)
            r = False
            while not r:
                r = self._attempt_to_place_ship(
                    choice(ascii_uppercase[: self.N]),
                    randint(1, self.N),
                    current_ship,
                    random() > 0.5,
                )
                max_attempts -= 1
                assert (
                    max_attempts
                ), "Max attempts exceeded, are you trying to place too many ships?"


class PlayerBoard(Board):
    def __init__(self, N, ships):
        super().__init__(N)
        self.place_ships(ships)

    def ask_for_coordinate(self):
        sym = ask_for_str(
            f"Please enter a column (A-{ascii_uppercase[self.N]})>>",
            ascii_uppercase[: self.N],
            modify=lambda x: x.upper(),
        )
        row = ask_for_int(f"Please enter a row (1-{self.N})>>", 1, self.N)
        orient = ask_for_orientation()
        return sym, row, orient

    def place_ships(self, ships):
        assert sum(ships) <= self.N**2, "No overals allowed!"
        while ships:
            self.print()
            current_ship = ships.pop(0)
            print(f"Placing ship of length {current_ship}")
            r = False
            while not r:
                sym, row, orient = self.ask_for_coordinate()
                r = self._attempt_to_place_ship(
                    sym,
                    row,
                    current_ship,
                    orient,
                )
                if not r:
                    print("Invalid location!")


def ask_for_int(prompt, low, high):
    assert low < high, "unpossible"
    while True:
        try:
            v = int(input(prompt))
        except ValueError:
            print("Invalid option!")
            continue
        if low <= v <= high:
            return v
        else:
            print("Outside range!")


def ask_for_str(prompt, options, modify=None):
    while True:
        sym = input(prompt)
        if modify is not None:
            sym = modify(sym)
        if sym in options:
            return sym
        else:
            print("This is not a valid option!")


def ask_for_orientation():
    while True:
        yn = input("Would you like to align horizontally? (y/n) >>").lower()
        if yn == "y":
            return True
        else:
            return False


N = 8
ships = [5, 4, 3, 2]
shuffle(ships)
boards = {"CPU": ComputerBoard(N, ships[:]), "Human": PlayerBoard(N, ships[:])}

for b in boards:
    print(b)
    boards[b].place_ships(ships)
    print("==")
    boards[b].print()
