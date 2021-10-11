#!/usr/bin/python
import sys
import RPi.GPIO as GPIO
from time import sleep
import os
import datetime
import threading

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # For the door hair switch
GPIO.setup(40, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # For the doorbell

try:

    def longButtonPress():
        print("LONG BUTTON RPESS")

    def shortButtonPress():
        print("SHORT BUTTON PRESSED")
        os.system("sudo node /home/pi/main/toggle.js")
    def doorOpened():
        print("Door has been opened - this message shouldnt appear until the door has been closed again!!! :0 ")
        os.system("sudo node /home/pi/main/toggle.js")

    def checkButtonPressed():      # Seperate thread to check button (long and short press)
        GPIO.setmode(GPIO.BOARD)
        counter = 0
        buttonJustPressed = False
        while True:
            if (GPIO.input(40) == True):
                counter = counter + 2
                buttonJustPressed = True

            elif (GPIO.input(40) == False) and (buttonJustPressed == True):
                if counter >= 40 :
                    longButtonPress()
                elif counter < 40 :
                    shortButtonPress()

                buttonJustPressed = False
                counter = 0

            sleep(0.1)                  # mandatory wait to stop CPU exploding

    def checkDoorOpened():      # Seperate thread to check door
        alreadyOpen = False
        while True:
            if (GPIO.input(37) == False) and (alreadyOpen == False):
                doorOpened()
                alreadyOpen = True
            elif (GPIO.input(37) == True) and (alreadyOpen == True):
                alreadyOpen = False

            sleep(0.1)                  # mandatory wait to stop CPU exploding

    doorThread = threading.Thread(target=checkDoorOpened, args=())
    buttonThread = threading.Thread(target=checkButtonPressed, args=())

    buttonThread.start()
    doorThread.start()

    buttonThread.join()
    doorThread.join()

# should only get to here if there is an error (E.g. user interupted)

finally:
    GPIO.cleanup()

