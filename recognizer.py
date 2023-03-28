import time
import speech_recognition as sr
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def tts_speak(my_text):
    with BytesIO() as f:
        gTTS(text=my_text, lang='en', tld="co.uk").write_to_fp(f)
        f.seek(0)
        song = AudioSegment.from_file(f, format="mp3")
        play(song)

def recognize(text, type):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        tts_speak(text)
        audio = r.record(source, duration = 3)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        recog = r.recognize_google(audio, language="de-DE")
        recog = recog.replace(" ", "")
        recog = recog[0].capitalize() + recog[1]
        if type == "pos":
            if recog[0] in ["A","B","C","D","E","F","G","H","I","J"] and int(recog[1]) >= 0 and int(recog[1]) < 10:
                return recog
            else:
                recognize("Wrong input, " + text, type)
        else:
            if recog == "horizontal":
                return 1
            elif recog == "vertikal":
                return 0
            else:
                recognize("Wriong input, "+ text, type)
    except sr.UnknownValueError:
        recognize("Error, " + text, type)
    except sr.RequestError as e:
        recognize("Error, " + text, type)