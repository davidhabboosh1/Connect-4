import serial
import time

# send the move to the arduino
def send_to_serial(col, ser):
    ser.write(f'{col}'.encode('utf-8'))
    time.sleep(5)