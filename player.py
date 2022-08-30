from enum import Enum


class Player(Enum):
    USER = 1
    CPU = 2
    NONE = 3

    def other_player(self):
        if self is Player.USER:
            return Player.CPU
        elif self is Player.CPU:
            return Player.USER
        else:
            return Player.NONE

    def __str__(self) -> str:
        if self is Player.USER:
            return "\x1b[31m" + "\N{LARGE CIRCLE}" + "\x1b[39m"
        elif self is Player.CPU:
            return "\x1b[33m" + "\N{LARGE CIRCLE}" + "\x1b[39m"
        else:
            return " "
