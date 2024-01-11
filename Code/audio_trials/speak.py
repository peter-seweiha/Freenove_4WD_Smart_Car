from gtts import gTTS 
import os 

language = 'en'
message = 'i love you'


# Text to Speech part
try:
    myobj = gTTS(text=message, lang=language, slow=False) 

    myobj.save("message.mp3") 

    os.system("afplay message.mp3") 
except:
    print('message did not work')
    pass