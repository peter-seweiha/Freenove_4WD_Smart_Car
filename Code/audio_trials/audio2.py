import speech_recognition as sr
from gtts import gTTS 
import os 
from Motor import *
import time


r = sr.Recognizer()
language = 'en'

# create functions for motor movement
def forward():
    PWM.setMotorModel(800,800,800,800)
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved forward'
    return message

def backward():
    PWM.setMotorModel(-800,-800,-800,-800)
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved backward'
    return message

def left():
    PWM.setMotorModel(-2000,-2000,4000,4000)
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved left'
    return message

def right():
    PWM.setMotorModel(4000,4000,-2000,-2000)
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved right'
    return message


def run_program():
    while True:
        message = ''
        phrase = ''
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            phrase = r.recognize_google(audio).lower()
            print(phrase)
        except sr.UnknownValueError:
            print("I do not understand")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        
        if 'forward' in phrase:
            message = forward()
        elif 'backward' in phrase:
            message = backward()
        elif 'left' in phrase:
            message = left()
        elif 'right' in phrase:
            message = right()
        elif 'dismissed' in phrase:
            break
        else:
            pass

            print(message)

        #Text to Speech part
        try:
            # get google txt t speech and save mp3 file
            myobj = gTTS(text=message, lang=language, slow=False) 
            myobj.save("message.mp3") 
            
            # ply mp3 file on dummy vlc and close it down
            os.system("vlc -I dummy message.mp3 vlc://quit")
        except:
            pass


print ('Program is starting ... ')
try:
    run_program()
except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    print('Program Ended')