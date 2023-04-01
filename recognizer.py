import time
import speech_recognition as sr
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# Methode für das Ausgeben von Text als Sprache
def tts_speak(my_text):
    # Erstellung eines Byte - Buffers mit BytesIO
    with BytesIO() as f:
        # Umwandlung des Texts in Sprache mit der gtts - Bibliothek
        gTTS(text=my_text, lang='en', tld="co.uk").write_to_fp(f)
        f.seek(0)
        # Konvertierung der Bytes zu einem abspielbaren Format
        song = AudioSegment.from_file(f, format="mp3")
        # Abspielen von Audio
        play(song)

# Methode für die Erkennung von Sprache
def recognize(text, type):
    r = sr.Recognizer()
    # man kann mittels dieser Methode alle funktionierenden Mikrophone ausgeben
    print(sr.Microphone.list_working_microphones())     
    # in_mic = input("Select a Microphone: ")
    # mic = sr.Microphone(device_index=int(in_mic))
    # Auswahl des Mikrophons
    with sr.Microphone() as source:   
        # Anpassung des Mikrophones an die Lautstärke in der Umgebung                  
        r.adjust_for_ambient_noise(source)              
        tts_speak(text)            
        # Aufnahme für 3 Sekunden                    
        audio = r.record(source, duration = 3)          

    # Spracherkennung mittels der Google Speech Recognition API
    try:
        # Verwendung der Google Speech Recognition API
        recog = r.recognize_google(audio, language="de-DE")
        # Umwandlung der Daten in das richtige Format
        recog = recog.replace(" ", "")
        recog = recog.upper()
        print(recog)
        # Rückgabe der umgewandelten Daten
        # Zuerst muss der Buchstabe und danach die Zahl des Feldes ausgesprochen werden
        if type == "pos":
            if recog[0] in ["A","B","C","D","E","F","G","H","I","J"] and int(recog[1]) >= 0 and int(recog[1]) < 10:
                return recog
            else:
                recognize(text, type)
        else:
            # Wenn es sich bei der Eingabe nicht um eine Position handelt, muss man entweder Horizontal ode Vertikal für die Richtung des 
            # Schiffs angeben
            if recog == "HORIZONTAL":
                return 1
            elif recog == "VERTIKAL":
                return 0
            else:
                recognize(text, type)
    # Sollten bei der Erkennung Fehler entstehen, wird die recognize - Methode erneut ausgeführt
    except sr.UnknownValueError:
        recognize(text, type)
    except sr.RequestError as e:
        recognize(text, type)