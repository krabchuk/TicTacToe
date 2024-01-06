from random import randint

class RandomAgent:
    def __init__(self, board_dim):
        self.board_dim = board_dim

    @staticmethod
    def get_move(board):
        available_cells = []
        for i in range(board.board_dim):
            for j in range(board.board_dim):
                if board.board[i][j][0] == 0:
                    available_cells.append((i,j))
        return available_cells[randint(0, len(available_cells) - 1)]