from string import ascii_uppercase
from random import random, choice

def create_empty_board(N):
  assert N > 0, "Cannot have a negative board size!"
  board = []
  for _ in range(N):
    row = []
    for _ in range(N):
      row.append(0)
    board.append(row)
  return board
  
def print_board(board, sep = "  "):
  N = len(board)
  
  print(sep, end=" ")
  for letter in ascii_uppercase[:N]:
    print(letter, end=sep)
  
  j = 1
  print("")
  for row in board:
    print(j, end=sep)
    j += 1
    for sym in row:
      print(sym, end=sep)
    print("")

def check_horizontal(board, sym, row, L):
  col = ascii_uppercase.index(sym)
  
  valid = 0 <= col <= N - L
  if not valid:
    return valid
  for j in range(col, col + L):
    if board[row-1][j] == 1:
      valid = False

  return valid

def check_vertical(board, sym, row, L):
  col = ascii_uppercase.index(sym)
  
  valid = 0 <= row <= N - L + 1

  if not valid:
    return valid
  for j in range(row, row + L):
    if board[j-1][col] == 1:
      valid = False

  return valid

def place_ship(board, sym, row, L, horizontal = True):
    if horizontal and check_horizontal(board, sym, row, L):
      col = ascii_uppercase.index(sym)
      for j in range(col, col + L):
        board[row-1][j] = 1
    elif not horizontal and check_vertical(board, sym, row, L):
      col = ascii_uppercase.index(sym)
      for j in range(row - 1, row + L - 1):
        board[j][col] = 1
    else:
      return False
    return True
  
N = 5
board = create_empty_board(N)
#ships = [2, 3, 4, 5]
#while ships:
#  current_ship = ships.pop(0)
#  r = False
#  while not r:
#    r = place_ship(board, choice(ascii_uppercase[:N]), choice(range(N)), current_ship, random() > 0.5)

place_ship(board, 'A', 1, 3)
   
print_board(board)
