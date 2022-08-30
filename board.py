from player import Player
from axis_offsets import Axis


class Board:
    ROWS = 6
    COLS = 7

    def __init__(self) -> None:
        self.grid = Board.make_board()
        self.bottom_row_for_col = [self.ROWS - 1 for _ in range(self.COLS)]
        self.played_count = 0

    def update_with_selection(self, selection, player, remove=False):
        column = selection - 1
        row = self.bottom_row_for_col[column]
        if remove:
            self.grid[row + 1][column] = Player.NONE
            self.bottom_row_for_col[column] += 1
            self.played_count -= 1
        else:
            self.grid[row][column] = player
            self.bottom_row_for_col[column] -= 1
            self.played_count += 1

    def line_score(self, selection, player):
        column = selection - 1
        row = self.bottom_row_for_col[column]
        max_in_row = 0
        for axis in Axis:
            in_row = self.get_num_in_row_for(player, row, column, axis)
            if in_row > max_in_row:
                max_in_row = in_row
            if max_in_row == 4:
                break
        return max_in_row

    def get_num_in_row_for(self, player, row, column, axis):
        def count_in_direction(dir):
            count = 0
            for n in range(1, 4):
                offset_row = row + (n * axis.value.row * dir)
                offset_col = column + (n * axis.value.column * dir)

                # bounds check
                if not ((0 <= offset_row < self.ROWS)
                        and (0 <= offset_col < self.COLS)):
                    break

                if self.grid[offset_row][offset_col] is player:
                    count += 1
                else:
                    break
            return count

        return (1 + count_in_direction(1) + count_in_direction(-1))

    @property
    def is_full(self):
        return self.played_count == self.ROWS * self.COLS

    @property
    def playable_columns(self):
        playable = []
        for column in range(self.COLS):
            if self.grid[0][column] is Player.NONE:
                playable.append(column + 1)
        return playable

    def __str__(self):
        board = ""
        for row in range(self.ROWS):
            player_chars = [str(self.grid[row][col])
                            for col in range(self.COLS)]
            board += "| " + " | ".join(player_chars) + " |\n"
        board += "-----------------------------\n"
        board += "  " + "   ".join([str(i) for i in range(1, 8)]) + "\n"
        return board

    @classmethod
    def make_board(cls):
        board = []
        for _ in range(cls.ROWS):
            row_list = []
            for _ in range(cls.COLS):
                row_list.append(Player.NONE)
            board.append(row_list)
        return board
