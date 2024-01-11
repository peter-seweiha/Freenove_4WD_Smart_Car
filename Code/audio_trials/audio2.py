import speech_recognition as sr
# from gtts import gTTS 
# import os 
from Motor import *
import time


r = sr.Recognizer()
language = 'en'

# create functions for motor movement
def forward():
    PWM.setMotorModel(700,700,700,700)
    time.sleep(0.5)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved forward'
    return message

def backward():
    PWM.setMotorModel(-700,-700,-700,-700)
    time.sleep(0.5)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved backward'
    return message

def left():
    PWM.setMotorModel(-2000,-2000,4000,4000)
    time.sleep(0.5)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved left'
    return message

def right():
    PWM.setMotorModel(4000,4000,-2000,-2000)
    time.sleep(0.5)
    PWM.setMotorModel(0,0,0,0)
    message = 'moved right'
    return message



# def switch_light(phrase):
#     if 'on' in phrase:
#         try:
#             ser.write(b"on\n")
#             message = 'Light is On'
#         except:
#             pass
#     elif 'off' in phrase:
#         try:
#             ser.write(b"off\n")
#             message = 'Light is Off'
#         except:
#             pass
#     else:
#         message = 'I dont understand what to do with the light'

#     return message

def run_program():
    while True:
        response = ''
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

        if "car" in phrase:  # name of the bot
            if 'forward' in phrase:
                response = forward()
            elif 'backward' in phrase:
                response = backward()
            elif 'left' in phrase:
                response = left(phrase)
            elif 'right' in phrase:
                response = right(phrase)
            elif 'dismissed' in phrase:
                break
            else:
                pass

            print(response)

            # Text to Speech part
            # try:
            #     myobj = gTTS(text=response, lang=language, slow=False) 

            #     myobj.save("response.mp3") 

            #     os.system("afplay response.mp3") 
            # except:
            #     pass


print ('Program is starting ... ')
try:
    run_program()
except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
