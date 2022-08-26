from enum import Enum

class Player(Enum):
  RED = 1
  YELLOW = 2
  EMPTY = 3

      
  def __str__(self) -> str:
    if self is Player.RED:
      return "\x1b[31m" + "\N{LARGE CIRCLE}" + "\x1b[39m"
    elif self is Player.YELLOW:
      return "\x1b[33m" + "\N{LARGE CIRCLE}" + "\x1b[39m"
    else:
      return " " #\N{BLACK LARGE CIRCLE}"