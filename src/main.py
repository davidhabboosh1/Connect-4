from Connect4Solver import Connect4Solver
import image2matrix as i2m
import time
import serial_motion as sm

if __name__ == '__main__':
    # initialize the board as an empty 6x7 matrix
    board = [[0 for _ in range(7)] for _ in range(6)]
    
    # initialize the game
    c4s = Connect4Solver(board)
    
    while True: # should be while game is not over
        # let the player move
        new_board = board
        while new_board == board:
            new_board = i2m.get_new_board()
            time.sleep(3)
            
        # update the board
        board = new_board
        c4s.update_state(board)
        
        # get the next move and make it
        next_move = c4s.next_move()
        # need to get new board here
        sm.move_to_col(next_move)
        sm.move_to_col(10) # drop the piece and move away
        time.sleep(10)