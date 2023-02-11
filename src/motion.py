# imports for gpio on raspberry pi
import RPi.GPIO as GPIO
import time

# set pins for motor controller
ena = 29
left1 = 31
enb = 32
left2 = 33
right1 = 35
right2 = 37

# attach pins to gpio
GPIO.setmode(GPIO.BOARD)
GPIO.setup(left1, GPIO.OUT)
GPIO.setup(left2, GPIO.OUT)
GPIO.setup(right1, GPIO.OUT)
GPIO.setup(right2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

# set the speeds of ena and enb to 100
GPIO.PWM(ena, 100).start(100)
GPIO.PWM(enb, 100).start(100)

# how long to run the motor for per column
TIME_BETWEEN = 0.5

# save the current position of the robot
current_col = -1

# move the motors to get to the given column
def move_to_column(column):
    global current_col
    fwd = column > current_col
    
    for _ in range(column - current_col):
        GPIO.output(left1, GPIO.HIGH if fwd else GPIO.LOW)
        GPIO.output(left2, GPIO.LOW if fwd else GPIO.HIGH)
        GPIO.output(right1, GPIO.HIGH if fwd else GPIO.LOW)
        GPIO.output(right2, GPIO.LOW if fwd else GPIO.HIGH)
        time.sleep(TIME_BETWEEN)
        
    GPIO.output(left1, GPIO.LOW)
    GPIO.output(right1, GPIO.LOW)
    
    current_col = column
    
# reset to the start position
def move_to_start():
    move_to_column(-1)
    
move_to_column(5)
GPIO.cleanup()