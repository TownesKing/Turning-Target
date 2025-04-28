import time
import RPi.GPIO as GPIO
import vlc as vlc

FileDirectory = "c/Desktop/Audio/files" #make sure to update

#pin allication for specific features
PinQuit = 1
PinRestart = 2
PinPause = 3
PinSkip = 4
PinNMC = 5
PinYes = 6
PinNo = 7

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

#  STATE # | name
#  0       | Start
#  1       | 3 minute prep
#  2       | NMC slow
#  3       | Cold range
#  4       | NMC Timed 1
#  5       | NMC Timed 2
#  6       | Timed Aliby string
#  7       | Cold Range Timed
#  8       | NMC Rapid 1
#  9       | NMC Rapid 2
#  10      | Rapid Aliby string
#  11      | Cold Range Rapid
#  12      | 
#  13      | 
#  14      | 
#  15      | 
#  16      | 
#  

audioPlayed = True
# O is none, 1 is move onto next, 2 is aliby
switchSate = 0
state = 0

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

def enterprete():
    num = decode()
    if num == PinQuit:
        return 1
    elif num == PinSkip:
        return 2
    elif num == PinYes:
        return 3
    elif num == PinNo:
        return 4
    else:
        return 0

def play(name):
    Media = vlc.MediaPlayer(FileDirectory + name + ".mp3")
    Media_Player.set_media(Media)
    Media_Player.play()

def audioUpdate(num):
    if(num == 1):
        if Media_Player.get_time() == Media_Player.get_length():
            Media_Player.stop()
            audioPlayed = True
    if (num == 2):
        Media_Player.stop()
        

def State3MinutePrep(state, switchSate, audioPlayed):
    if audioPlayed == True & switchSate == 0:
        play("3MinPrep")
        switchSate = 1
        audioPlayed = False
    if audioPlayed == True & switchSate == 1:
        play("Is everyone ready")
        switchSate == 2
        audioPlayed = False
    if audioPlayed == True & switchSate == 2:
        state = 2
        switchSate = 0
        audioPlayed = False

def StateNMCSlow(state, switchSate, audioPlayed):
    if audioPlayed == True & switchSate == 0:
        play("NMCSlowPrepToReady") #From anouncement to asking if ready
        switchSate = 1
        audioPlayed = False
    if switchSate == 2:
        if enterprete() == 3:
            switchSate = 3
        if enterprete() == 4:
            switchSate = 4
    if audioPlayed == True & switchSate == 3:
        play("NMCSlowIsReady")
        state = 3
        switchSate = 0
        audioPlayed = False
    if audioPlayed == True & switchSate == 4:
        play("NotReadyIsReady") # Line is not ready give 1 more minute then ask again
        switchSate = 1
        audioPlayed = False

while True:

    buton = enterprete()
    audioUpdate(1)

    #button inputs
    if buton > 0:
        if buton == PinQuit:
            break

    #states
    if state == 1:
        State3MinutePrep(state, switchSate, audioPlayed)
    if state == 2:
        StateNMCSlow(state, switchSate, audioPlayed)