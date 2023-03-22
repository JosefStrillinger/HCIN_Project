from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

class GTTSpeech():
    def __init__(self):
        self.name = "gtts_speech"
        
    def speech(self, text):
        with BytesIO() as f:
            gTTS(text=text, lang='en', tld="co.uk").write_to_fp(f)
            f.seek(0)
            song = AudioSegment.from_file(f, format="mp3")
            print(text)
            play(song)

