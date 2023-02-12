import serial
import RPi.GPIO as GPIO

ser = serial.Serial('/dev/ttyACM0', 9600)

# move to the given column -- 10 drops the piece and moves away
def move_to_col(column):
    ser.write(column + ord('a'))