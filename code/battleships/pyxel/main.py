import board as bd
import pyxel
from itertools import product

class PyxelBoard(bd.ComputerBoard):
    """
    Draw (and interact) with board
    """
    empty_col = 1
    filled_col = 3
    destroyed_col = 8
    def __init__(self, N, L, inner, outer):
        super().__init__(N, [5,4,3,2])
        self.N = N
        self.L = L
        self.inner = inner
        self.outer = outer

    def draw(self):
        pyxel.cls(0)
        for i,j in product(range(self.N), range(self.N)):
            if not self.board[i][j]:
                col = PyxelBoard.empty_col
            elif self.board[i][j] > 0:
                col = PyxelBoard.filled_col
            else:
                col = PyxelBoard.destroyed_col

            pyxel.rect(self.outer + i * (self.L + self.inner),
                       self.outer + j * (self.L + self.inner),
                       self.L, self.L, col)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x = (pyxel.mouse_x - self.outer) // (self.L + self.inner)
            y = (pyxel.mouse_y - self.outer) // (self.L + self.inner)
            if self.board[x][y]:
                # TODO - notify board change
                self.board[x][y] *= -1
            else:
                print("Miss!")


class Game:
    def __init__(self, N, L, inner, outer):
        screen_size = 2*outer + N * L + (N-1)*inner
        self.board = PyxelBoard(N, L, inner, outer)
        pyxel.init(screen_size, screen_size)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.board.update()

    def draw(self):
        pyxel.cls(0)
        self.board.draw()


if __name__ == "__main__":
    Game(12, 40, 5, 50)
