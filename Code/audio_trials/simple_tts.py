from gtts import gTTS 
import os 

language = 'en' # 'en'
message = "  yo yo saalwa, party in the house"


# Text to Speech part
try:
    myobj = gTTS(text=message, lang=language, slow=False, tld= 'us') 

    myobj.save("message.mp3") 

    os.system("cvlc message.mp3")
    
except:
    print('message did not work')
    pass
