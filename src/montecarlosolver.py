from montecarlosim import MonteCarloSimulation

class Connect4Solver:
    player = 1

    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],]
        self.last_move = None
        pass

    def updateState(self, board):
        self.board = board
        pass

    def nextMove(self):
        max_win_pct = 0
        win_pct = 0
        best_move = 0
        for i in range(7):
            win_pct = 0
            for j in range (2000):
                sim = MonteCarloSimulation(self.board, 1, i, j)
                win_pct += 1 if sim.run_sim() == 1 else 0
            win_pct = win_pct / 2000
            print(win_pct, i)
            if (win_pct > max_win_pct):
                best_move = i
            max_win_pct = max(max_win_pct, win_pct)
        return best_move

    def _solve(self):
        pass

    def winner(self):
        # 1 for 1
        # 2 for 2
        # 0 if no winner
        # this is easy
        # you uh, go to each kernel, or to each slot and like recur down 7
        # 6 * 7 = 42 * 4 = 168 
        pass
    
    
mm = Connect4Solver()
print(mm.nextMove())
