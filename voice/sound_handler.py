# THIS PROBABLY CAN BE DELETED
#
import speech_recognition as sr
from judylog.judylog import judylog
from gtts import gTTS
import pygame
from mutagen.mp3 import MP3
from io import BytesIO

class soundHandler:
    # Class for all audio recording as part of Judy
    def __init__(self, accent):
        #Initialize the microphone and recognizer
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.accent = accent

        # Adjust for the ambient noise
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

        print('\nsoundHandler.__init__ > Starting to listen...')

    def read_text(self, text):
        '''
        Simple function to read the users response.
        :param response:
        :return:
        '''
        print(f'soundHandler.read_text > Playing: {text}')
        spoken_accent = self.get_accent(self.accent)
        mp3_fp = BytesIO()
        myobj = gTTS(text=text, lang='en', slow=False, tld=spoken_accent)
        myobj.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        pygame.mixer.init()  # Initialize the mixer module
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

    @staticmethod
    def get_accent(accent):
        accent_map = {
            'australian': 'com.au',
            'english': 'co.uk',
            'american': 'us',
            'canadian': 'ca',
            'indian': 'co.in',
            'irish': 'ie',
            'south african': 'co.za',
            'nigerian': 'com.ng'
        }

        try:
            return accent_map[accent.lower()]
        except:
            judylog.error(f'judyVoice.get_accent > Unable to find accent ({accent}) in mapping.')
            return 'us'


    # def callback(self, recognizer, audio):
    #     try:
    #         if self.trigger_word in recognizer.recognize_sphinx(audio):
    #             print("Trigger!")
    #             self.trigger = True
    #         else:
    #             print(recognizer.recognize_sphinx(audio))
    #     except sr.UnknownValueError:
    #         print("Sphinx could not understand audio")
    #     except sr.RequestError as e:
    #         print("Could not request results from Sphinx; {0}".format(e))
    #
    # def listen_sphinx(self):
    #     with self.m as source:
    #         audio = self.r.listen(source)
    #
    #     try:
    #         if self.trigger_word in self.r.recognize_sphinx(audio):
    #             print("Trigger!")
    #             self.triggered = True
    #         else:
    #             print(self.r.recognize_sphinx(audio))
    #     except sr.UnknownValueError:
    #         print("Sphinx could not understand audio")
    #     except sr.RequestError as e:
    #         print("Could not request results from Sphinx; {0}".format(e))
    #
    # def transcribe_whisper(self):
    #     client = OpenAI()
    #
    #     audio_file = open("../temp/inputaudio.wav", "rb")
    #     transcription = client.audio.transcriptions.create(
    #         model="whisper-1",
    #         file=audio_file
    #     )
    #
    #     return(transcription.text)
    #
    # def wait_for_trigger(self):
    #     while self.triggered is False:
    #         self.listen_sphinx()
    #
    # def get_query(self):
    #     with self.m as source:
    #         self.r.adjust_for_ambient_noise(source)
    #         audio = self.r.listen(source)
    #
    #     with open("../temp/inputaudio.wav", "wb") as f:
    #         f.write(audio.get_wav_data())
    #
    #     transcription = self.transcribe_whisper()
    #     return transcription
    #
    #
    #
