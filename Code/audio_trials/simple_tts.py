from gtts import gTTS 
import os 

language = 'en'
message = 'how are you today mate? I hope you are doing very well!'


# Text to Speech part
try:
    myobj = gTTS(text=message, lang=language, slow=False, tld= 'co.uk') 

    myobj.save("message.mp3") 

    os.system("cvlc message.mp3")
    
except:
    print('message did not work')
    pass
