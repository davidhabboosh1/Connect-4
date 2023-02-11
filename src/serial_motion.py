import serial
import time
import RPi.GPIO as GPIO

# ser = serial.Serial('/dev/ttyACM0', 9600)

# move to the given column
# def move_to_col(column):
    # ser.write(column + ord('a'))
    
# reset
# move_to_col(10)

# time.sleep(2)
    
# move to column 5
# move_to_col(5)

# close the serial port
# ser.close()

SERVO_PWR = 4
SERVO_GND = 6
SERVO_PWM = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PWM, GPIO.OUT)

# set the servo to 0 degrees
pwm = GPIO.PWM(SERVO_PWM, 50)
pwm.start(0)

# set the servo to 90 degrees
pwm.ChangeDutyCycle(7.5)

# set the servo to 180 degrees
pwm.ChangeDutyCycle(12.5)

pwm.stop()
GPIO.cleanup()