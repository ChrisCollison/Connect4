import random

from os import system
from player import Player
from board import Board
from question import Question
from axis_offsets import Axis, Offset

class Connect4:
  IN_ROW = 4

  def __init__(self) -> None:
    self.board = Board()
    self.active_player = Player.RED

  def play(self):
    print(self.board)

    is_winner = False
    while not is_winner:
      if self.active_player is Player.RED:
        move = self.user_turn()
        is_winner = self.move_wins(move, Player.RED)
      else:
        is_winner = self.computer_turn()
        print(self.board)
      
      if is_winner:
        if self.active_player is Player.RED:
          print("Congratulations you won!")
        else:
          print("Unlucky you lost!")

      if self.active_player is Player.RED:
        self.active_player = Player.YELLOW
      else:
        self.active_player = Player.RED
      
  def user_turn(self):
    selection = Question.get_response_from_list(
      "Select the column to play: ",
      [str(col + 1) for col in self.board.playable_columns]
    )
    return self.board.update(Player.RED, int(selection))
  
  def computer_turn(self):
    move_options = [
      (self.board.get_top_empty_row(column), column)
      for column in self.board.playable_columns
    ]

    # Try to win first  
    for move in move_options:
      if self.move_wins(move, Player.YELLOW):
        self.board[move] = Player.YELLOW
        return True

    # Next block user winner
    for move in move_options:
      if self.move_wins(move, Player.RED):
        self.board[move] = Player.YELLOW
        return False
    
    #  Otherwise play random col for now until min-max
    self.board[random.choice(move_options)] = Player.YELLOW
    return False

  def winning_line(self, player, move, axis: Offset):
    row, column = move
    def count_in_direction(dir):
      count = 0 
      for n in range(1, 4):
        offset_row = row + (n * axis.value.row * dir)
        offset_col = column + (n * axis.value.column * dir)
        if self.board[offset_row, offset_col] is player:
          count += 1
        else:
          break
      return count

    return (1 + count_in_direction(1) + count_in_direction(-1)) >= 4

  
  def move_wins(self, move, player):
    winning_lines = []
    for axis in Axis:
      winning_lines.append(self.winning_line(player, move, axis))
    return any(winning_lines)


game = Connect4()
game.play()