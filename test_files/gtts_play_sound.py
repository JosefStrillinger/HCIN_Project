from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# To play audio text-to-speech during execution
def tts_speak(my_text):
    with BytesIO() as f:
        gTTS(text=my_text, lang='en', tld="co.uk").write_to_fp(f)
        f.seek(0)
        song = AudioSegment.from_file(f, format="mp3")
        play(song)

tts_speak("Oi mate, what the hell do you think you're doing")