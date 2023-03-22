import speech_recognition as sr

class SpeechRecognition():
    def __init__(self):
        self.speech_recog = sr.Recognizer()
    
    def recognize(self):
        with sr.Microphone() as source:
            self.speech_recog.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = self.speech_recog.record(source, duration = 5)
        try:
            recognized_text = self.speech_recog.recognize_google(audio, language="en-US")
            return recognized_text.lower()
        except sr.UnknownValueError:
            print("The audio couldn't be recognized, please try again")
        except sr.RequestError as e:
            print("Error: {0}".format(e))
