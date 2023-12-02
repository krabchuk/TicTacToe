from IPython.display import clear_output

import numpy as np

def show_field(field):
    n = len(field)
    remap = {0: ' ', 1: 'x', -1: 'o'}
    clear_output(wait=True)
    print('    ', end='')
    for i in range(n):
        print(f"{i}   ", end='')
    print()
    for i in range(n):
        print('    ', end='')
        print('-   ' * n)
        print(f"{i} | ", end='')
        print(' | '.join(map(lambda x: remap[x], field[i])) + ' |')
    print('    ' + '-   ' * n)

class Board:
    def __init__(self, board_dim=3, win_condition=None):
        self.board_dim = board_dim
        if win_condition is None:
            self.win_condition = board_dim
        else:
            self.win_condition = win_condition
        # 0: empty
        # 1: cross
        # -1: nought
        self.board = np.zeros((board_dim, board_dim))
        self.empty_cells = board_dim * board_dim

    def deepcopy(self):
        b = Board()
        b.board_dim = self.board_dim
        b.win_condition = self.win_condition
        b.empty_cells = self.empty_cells
        b.board = np.copy(self.board)
        return b

    def check_win(self, i, j):
        # vertical
        same_cell = 0
        k = i + 1
        while k < self.board_dim and self.board[k][j] == self.board[i][j]:
            same_cell += 1
            k += 1

        k = i - 1
        while k >= 0 and self.board[k][j] == self.board[i][j]:
            same_cell += 1
            k -= 1

        if same_cell == (self.win_condition - 1):
            return self.board[i][j]


        # horizontals
        same_cell = 0
        k = j + 1
        while k < self.board_dim and self.board[i][k] == self.board[i][j]:
            same_cell += 1
            k += 1

        k = j - 1
        while k >= 0 and self.board[i][k] == self.board[i][j]:
            same_cell += 1
            k -= 1

        if same_cell == (self.win_condition - 1):
            return self.board[i][j]

        # diagonals
        same_cell = 0
        k = i + 1
        l = j + 1
        while k < self.board_dim and l < self.board_dim and self.board[k][l] == self.board[i][j]:
            same_cell += 1
            k += 1
            l += 1

        k = i - 1
        l = j - 1
        while k >= 0 and l >= 0 and self.board[k][l] == self.board[i][j]:
            same_cell += 1
            k -= 1
            l -= 1

        if same_cell == (self.win_condition - 1):
            return self.board[i][j]

        same_cell = 0
        k = i + 1
        l = j - 1
        while k < self.board_dim and l >= 0 and self.board[k][l] == self.board[i][j]:
            same_cell += 1
            k += 1
            l -= 1

        k = i - 1
        l = j + 1
        while k >= 0 and l < self.board_dim and self.board[k][l] == self.board[i][j]:
            same_cell += 1
            k -= 1
            l += 1

        if same_cell == (self.win_condition - 1):
            return self.board[i][j]

        return 0

    def show(self):
        show_field(self.board)

    def make_move(self, move, player) -> int:
        i = move[0]
        j = move[1]
        if player not in [1, -1]:
            raise ValueError(f"Illegal player {player}")


        if self.board[i][j] != 0:
            return player * -1 # illegal move

        self.board[i][j] = player
        self.empty_cells -= 1

        win = self.check_win(i, j)
        if win != 0:
            self.empty_cells = 0

        return win