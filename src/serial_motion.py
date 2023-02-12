import serial
import time

# send the move to the arduino
def move(col, ser):
    ser.write(f'{6 - col}'.encode('utf-8'))
    time.sleep(3)
    
# reset the board
def reset(ser):
    ser.write('r'.encode('utf-8'))