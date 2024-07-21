from string import ascii_uppercase
from random import random, choice, shuffle
from itertools import cycle, pairwise, islice
from pprint import pprint

def circle(r):
    """
    >>> list(circle('abc'))
    [('a', 'b'), ('b', 'c'), ('c', 'a')]
    """
    yield from islice(pairwise(cycle(r)), len(r))

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
        self.empty()
        self.columns = ascii_uppercase[:N]
        self.rows = tuple(range(1, N + 1))


    def empty(self):
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]

    def print(self, sep="  "):
        for j, row in enumerate(self.board):
            if not j:
                itr = self.columns
            else:
                itr = row
            print(f"{j:2}", *(f"{i:>2}" for i in itr), sep=sep)

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

    def hit(self, sym, row):
        r = self.board[as_col(sym)][as_row(row)] > 0
        if r:
            self.board[as_col(sym)][as_row(row)] = 0
        return r

    def lost(self):
        for row in self.board:
            if any(v > 0 for v in row):
                return False
        return True


class ComputerBoard(Board):
    def __init__(self, N, ships):
        super().__init__(N)
        self.place_ships(ships)

    def place_ships(self, ships, max_attempts=50):
        assert sum(ships) <= self.N**2, "Impossible to fit!"
        while ships:
            current_ship = ships.pop(0)
            r = False
            while not r:
                r = self._attempt_to_place_ship(
                    choice(self.columns),
                    choice(self.rows),
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
            self.columns,
            modify=lambda x: x.upper(),
        )
        row = ask_for_int(f"Please enter a row (1-{self.N})>>", 1, self.N)
        orient = ask_for_orientation()
        return sym, row, orient

    def place_ships(self, ships):
        assert sum(ships) <= self.N**2, "Unpossible!"
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


class Player:
    def __init__(self, name, board):
        self.name = name
        self.board = board
        self.score = 0

    def attack(self, other) -> bool:
        """
        Which place to hit next?
        """
        pass


class IdiotComputerPlayer(Player):
    """
    Guesses Randomly
    """
    def __init__(self, name, board):
        super().__init__(name, board)

    def attack(self, other):
        sym = choice(self.board.columns)
        row = choice(self.board.rows)
        return other.board.hit(sym, row)


class DumbComputerPlayer(Player):
    """
    Shuffles all possible guesses with no repetitions
    """
    def __init__(self, name, board):
        super().__init__(name, board)
        self.moves = None

    def attack(self, other):
        if self.moves is None:
            self.moves = []
            for sym in other.board.columns:
                for row in other.board.rows:
                    self.moves.append((sym, row))
            shuffle(self.moves)
            self.j = 0
        elif self.moves:
            sym, row = self.moves.pop(0)
            return other.board.hit(sym, row)


class LessDumbComputerPlayer(Player):
    """
    Shuffle all possibilities and prioritises adjacent
    to hit locations
    """
    def __init__(self, name, board):
        super().__init__(name, board)
        self.moves = None

    def adjacent(self, sym, row):
        yield chr(ord(sym) - 1), row
        yield chr(ord(sym) + 1), row
        yield sym, row - 1
        yield sym, row + 1

    def attack(self, other):
        if self.moves is None:
            self.moves = []
            for sym in other.board.columns:
                for row in other.board.rows:
                    self.moves.append((sym, row))
            shuffle(self.moves)
            self.j = 0
        elif self.moves:
            sym, row = self.moves.pop(0)
            r = other.board.hit(sym, row)

            if r:
                for mov in self.adjacent(sym, row):
                    if mov not in self.moves:
                        continue
                    self.moves.pop(self.moves.index(mov))
                    self.moves.insert(0, mov)
            return r

class Game:
    def __init__(self, *players):
        self.players = list(players)

    def update(self):
        remaining_players = []
        while self.players:
            p = self.players.pop(0)
            if not p.board.lost():
                remaining_players.append(p)
            else:
                print(f"{p.name} loses with a score of {p.score}")

        self.players = remaining_players
        if len(self.players) <= 1:
            return True

        for a, b in circle(self.players):
            hit_q = a.attack(b)
            if hit_q:
                a.score += 1

    def play(self):
        while True:
            r = self.update()
            if not self.players:
                break
            if r:
                for p in self.players:
                    print(f"{p.name} wins with a score of {p.score}")
                    p.board.print()
                break


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    N = 8
    ships = [5, 4, 3, 2]

    g = Game(
        IdiotComputerPlayer("Idiot", ComputerBoard(N, ships[:])),
        LessDumbComputerPlayer("Less-dumb", ComputerBoard(N, ships[:])),
    )
    g.play()
