from connect4solver import Connect4Solver
import image2matrix as i2m
import time
import serial_motion as sm
import numpy as np
import serial

if __name__ == '__main__':
    # initialize the serial connection
    ser = serial.Serial('COM3', 9600)
    
    # send an r to the arduino to reset the board
    sm.reset(ser)
        
    # initialize the board as an empty 6x7 matrix
    board = [[0 for _ in range(7)] for _ in range(6)]
    
    # initialize the game
    c4s = Connect4Solver(1)
    
    while c4s.winner(board) == -1: # should be while game is not over
        print('Your turn\n')
        
        # let the player move, always with the yellow pieces
        new_board = board
        while new_board is None or (np.matrix(new_board) == np.matrix(board)).all():
            print('Take your turn...')
            new_board = i2m.get_new_board()
            time.sleep(3)
            
        print(f'{new_board}\n')
        
        # check if the game is over
        if (c4s.winner(board) != -1):
            break
        
        print('My turn\n')
            
        # update the board
        board = new_board
        c4s.update_state(board)
        
        # get the next move and make it
        next_move = c4s.next_move()
        board = c4s.board
        
        print(f'{board}\n')
        
        # have the robot drop the piece
        sm.move(next_move, ser)
        time.sleep(10)
    
    # tell the user the winner
    if c4s.winner(board) == 1:
        print('You lost :(')
    else:
        print('You won!')
        
    # close the serial connection
    ser.close()