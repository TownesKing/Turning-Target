import time
import RPi.GPIO as GPIO

clockOut = 10

outPin1 = 14
outPin2 = 15
outPin3 = 16
outPin4 = 17
outPin5 = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(outPin1, GPIO.OUT)
GPIO.setup(outPin2, GPIO.OUT)
GPIO.setup(outPin3, GPIO.OUT)
GPIO.setup(outPin4, GPIO.OUT)
GPIO.setup(outPin5, GPIO.OUT)

def encode(num):
    if (num < 32):
        binary = bin(num)[2:].zfill(5)

        if (bin & bin(1)[2:].zfill(5)) == bin(1)[2:].zfill(5):
            GPIO.output (outPin1, GPIO.HIGH)
        if (bin & bin(2)[2:].zfill(5)) == bin(2)[2:].zfill(5):
            GPIO.output (outPin2, GPIO.HIGH)
        if (bin & bin(4)[2:].zfill(5)) == bin(4)[2:].zfill(5):
            GPIO.output (outPin3, GPIO.HIGH)
        if (bin & bin(8)[2:].zfill(5)) == bin(8)[2:].zfill(5):
            GPIO.output (outPin4, GPIO.HIGH)
        if (bin & bin(16)[2:].zfill(5)) == bin(16)[2:].zfill(5):
            GPIO.output (outPin5, GPIO.HIGH)

        time.sleep(0.1)
        GPIO.output (clockOut, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output (clockOut, GPIO.LOW)
        GPIO.output (outPin1, GPIO.LOW)
        GPIO.output (outPin2, GPIO.LOW)
        GPIO.output (outPin3, GPIO.LOW)
        GPIO.output (outPin4, GPIO.LOW)
        GPIO.output (outPin5, GPIO.LOW)

def decomde():
    
        