#!/usr/bin/python
import sys
import RPi.GPIO as GPIO
import time
import os
import datetime

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)
# Set up GPIO 37 as input (for the door hairline switch)

GPIO.setup(37, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # For the door hair switch
GPIO.setup(40, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # For the doorbell

try:
    x = y = 0
    while True:
        if GPIO.input(37) == False:
            print(str(x) + " From the door");x=x+1
        if GPIO.input(40) == True:
            print(str(y) + " Button!!")     ;y=y+1
        time.sleep(0.1)
finally:
    GPIO.cleanup()
