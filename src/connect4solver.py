import random
import copy

class Connect4Solver(object):
    
    def __init__(self, turn):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],]
        self.turn = turn
    
    def heuristic(self, board):
        heur = 0
        state = board
        for i in range(0, len(board[0])):
            for j in range(0, len(board)):
                # check horizontal streaks
                try:
                    # add player one streak scores to heur
                    if state[i][j] == state[i + 1][j] == 1:
                        heur += 10
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 1:
                        heur += 100
                    if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j] == 1:
                        heur += 10000

                    # subtract player two streak score to heur
                    if state[i][j] == state[i + 1][j] == 2:
                        heur -= 10
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 2:
                        heur -= 100
                    if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j] == 2:
                        heur -= 10000
                except IndexError:
                    pass

                # check vertical streaks
                try:
                    # add player one vertical streaks to heur
                    if state[i][j] == state[i][j + 1] == 1:
                        heur += 10
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 1:
                        heur += 100
                    if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3] == 1:
                        heur += 10000

                    # subtract player two streaks from heur
                    if state[i][j] == state[i][j + 1] == 2:
                        heur -= 10
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 2:
                        heur -= 100
                    if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3] == 2:
                        heur -= 10000
                except IndexError:
                    pass

                # check positive diagonal streaks
                try:
                    # add player one streaks to heur
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == 1:
                        heur += 100
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 1:
                        heur += 100
                    if not j + 3 > 6 and state[i][j] == state[i+1][j + 1] == state[i+2][j + 2] \
                            == state[i+3][j + 3] == 1:
                        heur += 10000

                    # add player two streaks to heur
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == 2:
                        heur -= 100
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 2:
                        heur -= 100
                    if not j + 3 > 6 and state[i][j] == state[i+1][j + 1] == state[i+2][j + 2] \
                            == state[i+3][j + 3] == 2:
                        heur -= 10000
                except IndexError:
                    pass

                # check negative diagonal streaks
                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == 1:
                        heur += 10
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] == 1:
                        heur += 100
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] \
                            == state[i+3][j - 3] == 1:
                        heur += 10000

                    # subtract player two streaks
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == 2:
                        heur -= 10
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] == 2:
                        heur -= 100
                    if not j - 3 < 0 and state[i][j] == state[i+1][j - 1] == state[i+2][j - 2] \
                            == state[i+3][j - 3] == 2:
                        heur -= 10000
                except IndexError:
                    pass
        return heur

    # Returns the winner of the game
    def winner(self, board):
        # Check rows
        for row in board:
            for i in range(len(row) - 3):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != 0:
                    return row[i]

        # Check columns
        for col in range(len(board[0])):
            for i in range(len(board) - 3):
                if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] and board[i][col] != 0:
                    return board[i][col]

        # Check diagonals
        for row in range(len(board) - 3):
            for col in range(len(board[0]) - 3):
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] and board[row][col] != 0:
                    return board[row][col]

        for row in range(len(board) - 3):
            for col in range(3, len(board[0])):
                if board[row][col] == board[row + 1][col - 1] == board[row + 2][col - 2] == board[row + 3][col - 3] and board[row][col] != 0:
                    return board[row][col]

        # Check if board is full
        numPieces = 0
        for row in board:
            for col in row:
                if col == 1 or col == 2:
                    numPieces += 1
        
        if numPieces == 42:
            return 0

        return -1
    
    # Makes the next best move based off the minmax algorithm
    def _make_move(self, board, depth, maximizingPlayer):
        # if depth == 0 or game is over in position:
        #     return the heuristic value of position
        if depth == 0 or self.winner(board) != -1:
            return self.heuristic(board), 0
        if maximizingPlayer:
            value = -1000000
            for i in range(7):
                board_copy = copy.deepcopy(board)
                land = self._exec_move(board_copy, i)
                if land == -1:
                    continue
                else:
                    board_copy[land][i] = self.turn
                    (next_val, b_move) = self._make_move(board_copy, depth - 1, False)
                    if next_val > value:
                        value = next_val
                        best_move = i
            return value, best_move
        else:
            value = 1000000
            for i in range(7):
                board_copy = copy.deepcopy(board)
                land = self._exec_move(board_copy, i)
                if land == -1:
                    continue
                else:
                    board_copy[land][i] = (2 if self.turn == 1 else 1)
                    (next_val, b_move) = self._make_move(board_copy, depth - 1, True)
                    if next_val < value:
                        value = next_val
                        best_move = i
            return value, best_move

    def _exec_move(self, board, move):
        if board[5][move] == 0:
            return 5

        land = 0
        for i in range(6):
            if board[i][move] != 0:
                land = i - 1
                break

        return land


mm = Connect4Solver(1)

print(mm._make_move([ [0, 0, 0, 1, 0, 0, 0],
                      [1, 0, 0, 1, 0, 0, 0],
                      [1, 0, 0, 1, 0, 0, 0],
                      [2, 2, 0, 2, 0, 0, 0],
                      [1, 1, 0, 2, 0, 0, 0],
                      [1, 1, 1, 2, 2, 0, 0],], 5, True))