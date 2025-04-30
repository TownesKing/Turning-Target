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
#  3       | NMC Timed
#  4       | 
#  5       | 
#  6       | 
#  7       | 
#  8       | 
#  9       | 
#  10      | 
#  11      | 
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
Aliby = False

Media_Player = vlc.MediaPlayer()

#Intakes an integer and turns it into a signal that is encoded into binary, with PCB it swiches the state untill power is turned off to the board
def encode(num):
    if (num < 32):
        binary = bin(num)[2:].zfill(5) #Convert the number to a binary number from an integer

        GPIO.output (outPin1, GPIO.LOW)
        GPIO.output (outPin2, GPIO.LOW)
        GPIO.output (outPin3, GPIO.LOW)
        GPIO.output (outPin4, GPIO.LOW)
        GPIO.output (outPin5, GPIO.LOW)

        #Basically this takes the binary number cuts of the first two bits that indicate the number is in binar, now thier is just the up to 5 bits, 
        #We then mask this with the & oporation with one of each bit prepared in the same way, if the output of the mask is positive then a bit exists their, we also use zfill to add in 0's if the number is too short.
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

        #To write data we need to flash the clock signal to tell everythin to update so we wait 1/1000 of a second to let all the pins turn all the way on, then we flash the clock for another 1/1000 of a second, so the cycle the clock it takes 1/500 of a second
        time.sleep(0.001)
        GPIO.output (clockOut, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output (clockOut, GPIO.LOW)
        GPIO.output (outPin1, GPIO.LOW)
        GPIO.output (outPin2, GPIO.LOW)
        GPIO.output (outPin3, GPIO.LOW)
        GPIO.output (outPin4, GPIO.LOW)
        GPIO.output (outPin5, GPIO.LOW)

#outputs a integer based on what pins are sending data into the input pins listed by inPin variables, this is based on the PCB it is atached to for sending active low signals.
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

#Reads the input pins and retunrs a number based on what is input, this should only be used for complex fuctions, try to use decode more.
def enterprete():
    num = decode()
    if num == PinQuit:
        return 1
    elif num == PinSkip:
        return 2
    else:
        return 0

#Plays an audio file with the name input that is in the folder named in FileDirectory variable
def play(name):
    Media = vlc.MediaPlayer(FileDirectory + name + ".mp3")
    Media_Player.set_media(Media)
    Media_Player.play()

#This Function checks the current audio file and closes the application of it is over with a 1 or if 2 is imput then we just close it no questions asked
def audioUpdate(num):
    if(num == 1):
        if Media_Player.get_time() == Media_Player.get_length():
            Media_Player.stop()
            audioPlayed = True
    if (num == 2):
        Media_Player.stop()
        
#3 Minute prep period
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
        play("PlaceSlowTarget")
        state = 2
        switchSate = 0
        audioPlayed = False

#Slow with a is line ready
def StateNMCSlow():
    global state
    global switchSate
    global audioPlayed
    if switchSate == 2:
        if decode() == PinSkip:
            audioUpdate(2)
    if audioPlayed == True & switchSate == 0:
        play("NMCSlowPrepToReady") #From anouncement to asking if ready
        switchSate = 1
        audioPlayed = False
    if switchSate == 1:
        if decode() == PinYes:
            switchSate = 2
        if decode() == PinNo:
            switchSate = 3
    if audioPlayed == True & switchSate == 2:
        play("NMCSlowIsReady")
        switchSate = 4
        audioPlayed = False
    if audioPlayed == True & switchSate == 3:
        play("NotReadyIsReady") # Line is not ready give 1 more minute then ask again
        switchSate = 1
        audioPlayed = False
    if audioPlayed == True & switchSate == 4:
        play("RetraveAndReplaceTargesTimed")
        switchSate = 0
        state = 3
        audioPlayed = False

#Timed Fire
def StateNMCTimed():
    global state
    global switchSate
    global audioPlayed
    global Aliby
    if audioPlayed == True & switchSate == 0:
            play("NMCTimedPrepToReady") #From anouncement to asking if ready
            switchSate = 1
            audioPlayed = False
    if switchSate == 1:
        if decode() == PinYes:
            switchSate = 2
        if decode() == PinNo:
            switchSate = 3
    if audioPlayed == True & switchSate == 2:
        play("NMCTimedIsReadyAndString1")
        switchSate = 4
        audioPlayed = False
    if audioPlayed == True & switchSate == 3:
        play("NotReadyIsReady") # Line is not ready give 1 more minute then ask again
        switchSate = 1
        audioPlayed = False
    if switchSate == 4:
        if audioPlayed == True:
            play("Aliby?")
            audioPlayed = False
        if decode() == PinYes:
            audioUpdate(2)
            play("TheirIsAnAliby")
            Aliby = True
            audioPlayed = False
            switchSate = 5
        if decode() == False:
            audioUpdate(2)
            switchSate = 5
    if audioPlayed == True & switchSate == 5:
        play("TimedString2")
        switchSate = 6
        audioPlayed = False
    if switchSate == 6:
        if decode() == PinYes:
            switchSate = 8
        if decode() == PinNo:
            switchSate = 9
    if audioPlayed == True & switchSate == 8:
        play("NMCTimedIsReadyAndString2")
        switchSate = 10
        audioPlayed = False
    if audioPlayed == True & switchSate == 9:
        play("NotReadyIsReady") # Line is not ready give 1 more minute then ask again
        switchSate = 1
        audioPlayed = False
    if switchSate == 10:
        if audioPlayed == True:
            play("Aliby?")
            audioPlayed = False
        if decode() == PinYes:
            audioUpdate(2)
            play("TheirIsAnAliby")
            Aliby = True
            audioPlayed = False
            switchSate = 11
        if decode() == False:
            audioUpdate(2)
            switchSate = 11
    if switchSate == 11:
        if Aliby == True:
            if audioPlayed == True:
                play("AlibyStringNowToReady")
                audioPlayed = False
                switchSate = 13
        if Aliby == False:
            switchSate = 12
    if audioPlayed == True & switchSate == 12:
        play("RetreaveTargetsConcludeMatch")
        switchSate = 0
        audioPlayed = False
    if switchSate == 13:
        if decode() == PinYes:
            switchSate = 14
        if decode() == PinNo:
            switchSate = 15
    if audioPlayed == True & switchSate == 14:
        play("NMCTimedIsReadyAndAlibyString")
        audioPlayed = False
        switchSate = 12
    if audioPlayed == True & switchSate == 15:
        play("NotReadyIsReady")
        switchSate = 13
        audioPlayed == True

#Rapid Fire
def StateNMCRapid():
    global state
    global switchSate
    global audioPlayed
    global Aliby
    if audioPlayed == True & switchSate == 0:
            play("NMCRapidPrepToReady") #From anouncement to asking if ready
            switchSate = 1
            audioPlayed = False
    if switchSate == 1:
        if decode() == PinYes:
            switchSate = 2
        if decode() == PinNo:
            switchSate = 3
    if audioPlayed == True & switchSate == 2:
        play("NMCRapidIsReadyAndString1")
        switchSate = 4
        audioPlayed = False
    if audioPlayed == True & switchSate == 3:
        play("NotReadyIsReady") # Line is not ready give 1 more minute then ask again
        switchSate = 1
        audioPlayed = False
    if switchSate == 4:
        if audioPlayed == True:
            play("Aliby?")
            audioPlayed = False
        if decode() == PinYes:
            audioUpdate(2)
            play("TheirIsAnAliby")
            Aliby = True
            audioPlayed = False
            switchSate = 5
        if decode() == False:
            audioUpdate(2)
            switchSate = 5
    if audioPlayed == True & switchSate == 5:
        play("RapidString2")
        switchSate = 6
        audioPlayed = False
    if switchSate == 6:
        if decode() == PinYes:
            switchSate = 8
        if decode() == PinNo:
            switchSate = 9
    if audioPlayed == True & switchSate == 8:
        play("NMCRapidIsReadyAndString2")
        switchSate = 10
        audioPlayed = False
    if audioPlayed == True & switchSate == 9:
        play("NotReadyIsReady") # Line is not ready give 1 more minute then ask again
        switchSate = 1
        audioPlayed = False
    if switchSate == 10:
        if audioPlayed == True:
            play("Aliby?")
            audioPlayed = False
        if decode() == PinYes:
            audioUpdate(2)
            play("TheirIsAnAliby")
            Aliby = True
            audioPlayed = False
            switchSate = 11
        if decode() == False:
            audioUpdate(2)
            switchSate = 11
    if switchSate == 11:
        if Aliby == True:
            if audioPlayed == True:
                play("AlibyStringNowToReady")
                audioPlayed = False
                switchSate = 13
        if Aliby == False:
            switchSate = 12
    if audioPlayed == True & switchSate == 12:
        play("RetreaveTargetsConcludeMatch")
        switchSate = 0
        audioPlayed = False
    if switchSate == 13:
        if decode() == PinYes:
            switchSate = 14
        if decode() == PinNo:
            switchSate = 15
    if audioPlayed == True & switchSate == 14:
        play("NMCRapidIsReadyAndAlibyString")
        audioPlayed = False
        switchSate = 12
    if audioPlayed == True & switchSate == 15:
        play("NotReadyIsReady")
        switchSate = 13
        audioPlayed == True

while True:

    buton = decode()
    audioUpdate(1)

    #button inputs
    if buton > 0:
        if buton == PinQuit:
            break

    #states
    if state == 1:
        State3MinutePrep
    if state == 2:
        StateNMCSlow
    if state == 3:
        StateNMCTimed
    if state == 4:
        StateNMCRapid