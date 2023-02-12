from connect4solver import Connect4Solver
import image2matrix as i2m
import time
import serial_motion as sm
import numpy as np
import serial

if __name__ == '__main__':
    # initialize the board as an empty 6x7 matrix
    board = [[0 for _ in range(7)] for _ in range(6)]
    
    # initialize the game
    c4s = Connect4Solver(1)
    
    # initialize the serial connection
    ser = serial.Serial('COM3', 9600)
    
    while c4s.winner(board) == -1: # should be while game is not over
        print('Your turn')
        
        # let the player move, always with the yellow pieces
        new_board = board
        while (np.matrix(new_board) == np.matrix(board)).all():
            new_board = i2m.get_new_board()
            time.sleep(3)
            print('Take your turn...')
            
        print('My turn')
            
        # update the board
        board = new_board
        c4s.update_state(board)
        
        # get the next move and make it
        next_move = c4s.next_move()
        board = c4s.board
        
        # have the robot drop the piece
        sm.send_to_serial(next_move, ser)
        time.sleep(10)
    
    # tell the user the winner
    if c4s.winner(board) == 1:
        print('You won!')
    else:
        print('You lost :(')
        
    # close the serial connection
    ser.close()