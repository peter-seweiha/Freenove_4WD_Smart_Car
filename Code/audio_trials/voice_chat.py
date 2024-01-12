import speech_recognition as sr
from gtts import gTTS 
import os 
import time

import openai
from openai import OpenAI

# Paste OpenAI API key
os.environ["OPENAI_API_KEY"] = ''


r = sr.Recognizer()
language = 'en'


# create functions to get a message from ChatGPT

def get_message(phrase):
    client = OpenAI()
    
    chat_completion =  client.chat.completions.create(

    model='gpt-3.5-turbo-1106',
    messages = [
        {'role': 'system', 'content': "you are an a chatting friend to a 9 years old girl named 'Noor', try to be chatty, funny and a bit cheecky when you respond to her questions and use her name when you get a chance  "},
        {'role': 'assistant', 'content':"answer in less than 30 words" },
        {'role': 'user', 'content': phrase}

    ])
    
    message = chat_completion.choices[0].message.content
    print(message)
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

        
        if len(phrase)> 1 : # if the phrase is long enough
            message = get_message(phrase)
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