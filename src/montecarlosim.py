import random
import copy

class MonteCarloSimulation:

    def __init__(self, board, turn, move, i):
        self.board = copy.deepcopy(board)
        self._make_move(move)
        self.turn = turn # 1 or 2

    # -> int (who won)
    def run_sim(self):
        winner = self.winner()
        while winner == -1:
            move = random.randrange(0, 7)
            # find landing height
            # if height is -1
            land = self._make_move(move)
            if land == -1:
                continue
            else:
                self.board[land][move] = self.turn
            self.turn = (2 if self.turn == 1 else 1)
            winner = self.winner()
        
        return winner

    def _make_move(self, move):
        if self.board[5][move] == 0:
            return 5

        land = 0
        for i in range(6):
            if self.board[i][move] != 0:
                land = i - 1
                break

        return land

    def winner(self):
        # Check rows
        for row in self.board:
            for i in range(len(row) - 3):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != 0:
                    return row[i]

        # Check columns
        for col in range(len(self.board[0])):
            for i in range(len(self.board) - 3):
                if self.board[i][col] == self.board[i + 1][col] == self.board[i + 2][col] == self.board[i + 3][col] and self.board[i][col] != 0:
                    return self.board[i][col]

        # Check diagonals
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3] and self.board[row][col] != 0:
                    return self.board[row][col]

        for row in range(len(self.board) - 3):
            for col in range(3, len(self.board[0])):
                if self.board[row][col] == self.board[row + 1][col - 1] == self.board[row + 2][col - 2] == self.board[row + 3][col - 3] and self.board[row][col] != 0:
                    return self.board[row][col]

        # Check if board is full
        numPieces = 0
        for row in self.board:
            for col in row:
                if col == 1 or col == 2:
                    numPieces += 1
        
        if numPieces == 42:
            return 0

        return -1

