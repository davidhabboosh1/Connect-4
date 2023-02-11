import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

# move to the given column
def move_to_col(column):
    ser.write(column + ord('a'))
    
# reset
move_to_col(10)

time.sleep(2)
    
# move to column 5
move_to_col(5)

# close the serial port
ser.close()