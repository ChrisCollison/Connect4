from collections import namedtuple
from os import system, name as sys_type

from player import Player
from board import Board
from question import Question



Selection = namedtuple('Selection', ['column', 'is_winner', 'score'])


class Connect4:
    IN_ROW = 4
    LOOK_AHEAD = 3

    def __init__(self) -> None:
        self.board = Board()
        self.active_player = Player.USER
        self.winner = None

    def play(self):
        self.clear_terminal()
        print(self.board)

        while self.winner is None and not self.board.is_full:
            if self.active_player is Player.USER:
                self.user_turn()
            else:
                self.computer_turn()

            self.clear_terminal()
            print(self.board)
            self.active_player = self.active_player.other_player()

        self.declare_winner()

    def user_turn(self):
        selection = Question.get_response_from_list(
            "Select the column to play: ",
            [str(col) for col in self.board.playable_columns]
        )
        selection = int(selection)
        # before update
        will_win = self.board.line_score(selection, Player.USER) >= self.IN_ROW
        self.board.update_with_selection(selection, Player.USER)

        if will_win:
            self.winner = Player.USER

    def computer_turn(self):
        best_selection = None
        columns_scores = []
        cpu_wins = False
        player = Player.CPU
        played = []

        for turn in range(self.LOOK_AHEAD):
            # Guard board full
            if self.board.is_full:
                break

            look_ahead_selection = None
            turn_column_scores = []
            other = player.other_player()

            for column in self.board.playable_columns:
                player_line_score = self.board.line_score(column, player)
                player_wins = player_line_score >= self.IN_ROW
                other_wins = self.board.line_score(
                    column, other) >= self.IN_ROW
                turn_column_scores.append((player_line_score, column))

                if player_wins or other_wins:
                    look_ahead_selection = column
                    if player is Player.CPU and turn == 0:
                        cpu_wins = True
                    if player_wins and player is Player.USER:
                        # set score negative as user will win
                        columns_scores[-1][1] = -1
                    if player_wins or (other_wins and turn == 0):
                        best_selection = column
                    break

            if turn == 0:
                columns_scores = [*turn_column_scores]

            if best_selection is None:
                if look_ahead_selection is None:
                    look_ahead_selection = sorted(
                        turn_column_scores, reverse=True)[0][1]
                played.append(look_ahead_selection)
                self.board.update_with_selection(look_ahead_selection, player)
                player = player.other_player()
            else:
                break

        # Reverting the simulated moves to return board to original state
        for selection in played:
            self.board.update_with_selection(
                selection, Player.NONE, remove=True)

        if best_selection is None:
            best_selection = sorted(turn_column_scores, reverse=True)[0][1]

        self.board.update_with_selection(best_selection, Player.CPU)
        if cpu_wins:
            self.winner = Player.CPU

    def declare_winner(self):
        if self.winner is Player.USER:
            print("Congratulations you won!")
        elif self.winner is Player.CPU:
            print("Unlucky you lost - what a plonker you are!!")
        else:
            print("It's a tie!")

    def clear_terminal(self):
        # for windows
        if sys_type == 'nt':
            system('cls')

        # for mac and linux
        else:
            system('clear')


def main():
    game = Connect4()
    game.play()


if __name__ == "__main__":
    main()
