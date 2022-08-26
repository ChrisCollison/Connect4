from player import Player
from os import system

class Board:
  ROWS = 6
  COLS = 7

  def __init__(self) -> None:
    self.grid = Board.make_board()

  def get_top_empty_row(self, column):
    for row in range(self.ROWS - 1, -1, -1):
      if self.grid[row][column] is Player.EMPTY:
        return row
    raise ValueError("Shouldn't be called if not a known playable column")

  def update(self, player, selection):
    column = selection - 1
    row = self.get_top_empty_row(column)
    self.grid[row][column] = player
    print(self)
    return row, column

  @property
  def playable_columns(self):
    playable = []
    for column in range(self.COLS):
      if self.grid[0][column] is Player.EMPTY:
        playable.append(column)
    return playable

  def __str__(self):
    board = ""
    for row in range(self.ROWS):
      player_chars = [str(self.grid[row][col]) for col in range(self.COLS)]
      board += "| " + " | ".join(player_chars) + " |\n"
      
    board += "-----------------------------\n"
    board += "  " + "   ".join([str(i) for i in range(1,8)]) + "\n"
    system('clear')
    return board
   

  def __getitem__(self, position):
    Board.validate_position(position)
    row, column = position
    if (0 <= row < self.ROWS) and (0 <= column < self.COLS):
      return self.grid[position[0]][position[1]]
    else:
      return Player.EMPTY

  def __setitem__(self, position, newValue):
    Board.validate_position(position)

    if not isinstance(newValue, Player):
      raise ValueError("New value must be a Player")

    self.grid[position[0]][position[1]] = newValue
  
  @classmethod
  def validate_position(cls, position):
    if (
      not isinstance(position, tuple)
      or len(position) != 2
      or any([not isinstance(e, int) for e in position])
    ):
      raise TypeError("Invalid indices. Use [int, int]")
    return True
  
  @classmethod
  def make_board(cls):
    board =[]
    for _ in range(cls.ROWS):
      row_list = []
      for _ in range(cls.COLS):
        row_list.append(Player.EMPTY)
      board.append(row_list)
    return board

