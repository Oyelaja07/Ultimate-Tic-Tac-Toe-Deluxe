from settings import WINNING_POSITIONS


class TicTacToeGame:
    def __init__(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.move_history = []

    def reset(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.move_history = []

    def make_move(self, position, symbol=None):
        if not 0 <= position <= 8:
            return False

        if self.board[position] != "":
            return False

        symbol = symbol or self.current_player
        self.board[position] = symbol
        self.move_history.append((position, symbol))
        return True

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, symbol):
        for first, second, third in WINNING_POSITIONS:
            if (
                self.board[first] == symbol
                and self.board[second] == symbol
                and self.board[third] == symbol
            ):
                return first, second, third
        return None

    def is_draw(self):
        return "" not in self.board and not self.check_winner("X") and not self.check_winner("O")

    def available_moves(self):
        return [index for index, value in enumerate(self.board) if value == ""]

    def undo_last_move(self):
        if not self.move_history:
            return None

        position, symbol = self.move_history.pop()
        self.board[position] = ""
        self.current_player = symbol
        return position, symbol
