import serial

ser = serial.Serial('COM3', 9600)

# move to the given column
def move_to_col(column):
    ser.write(column)
    
# move to column 5
move_to_col(5)

# close the serial port
ser.close()