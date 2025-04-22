import time
import RPi.GPIO as GPIO
import vlc as vlc

FileDirectory = "c/Desktop/Audio/files" #make sure to update

clockOut = 10

outPin1 = 14
outPin2 = 15
outPin3 = 16
outPin4 = 17
outPin5 = 18

inPin1 = 19
inPin2 = 20
inPin3 = 21
inPin4 = 22
inPin5 = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(outPin1, GPIO.OUT)
GPIO.setup(outPin2, GPIO.OUT)
GPIO.setup(outPin3, GPIO.OUT)
GPIO.setup(outPin4, GPIO.OUT)
GPIO.setup(outPin5, GPIO.OUT)

GPIO.setup(inPin1, GPIO.IN)
GPIO.setup(inPin2, GPIO.IN)
GPIO.setup(inPin3, GPIO.IN)
GPIO.setup(inPin4, GPIO.IN)
GPIO.setup(inPin5, GPIO.IN)

Media_Player = vlc.MediaPlayer()

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

def decode():
    num = 0
    
    if GPIO.input (inPin1) == GPIO.LOW:
        num += 1
    if GPIO.input (inPin2) == GPIO.LOW:
        num += 2
    if GPIO.input (inPin3) == GPIO.LOW:
        num += 4
    if GPIO.input (inPin4) == GPIO.LOW:
        num += 8
    if GPIO.input (inPin5) == GPIO.LOW:
        num += 16
    
    return(num)

def play(name):
    Media = vlc.MediaPlayer(FileDirectory + name + ".mp3")
    Media_Player.set_media(Media)
    Media_Player.play()

def audioUpdate():
    if Media_Player.get_time() == Media_Player.get_length():
        Media_Player.stop()