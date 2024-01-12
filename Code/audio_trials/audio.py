import speech_recognition as sr


with sr.Microphone() as source:
    recognizer = sr.Recognizer()
    recognizer.adjust_for_ambient_noise(source)
    recognizer.dynamic_energy_threshold = 3000
    
    try:
        print('Litening ...')
        audio = recognizer.listen(source, timeout=5.0)
        response = recognizer.recognize_google(audio)
        print(response)
        
    except sr.UnknownValueError:
        print('Didn not recognize that.')
