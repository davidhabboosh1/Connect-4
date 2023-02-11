# imports for gpio on raspberry pi
import RPi.GPIO as GPIO

# set pins for motor controller
ena = 29
left1 = 31
left2 = 33
right1 = 35
right2 = 37
enb = 38

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

# drive the motors forward
GPIO.output(left1, GPIO.HIGH)
GPIO.output(left2, GPIO.LOW)
GPIO.output(right1, GPIO.HIGH)
GPIO.output(right2, GPIO.LOW)

GPIO.cleanup()