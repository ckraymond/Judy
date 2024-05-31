import speech_recognition as sr
from openai import OpenAI

class soundProcessing:
    # Class for all audio recording as part of Judy
    def __init__(self):
        self.freq = 44100
        self.duration = None
        self.filename = None
        self.trigger_word = 'judy'
        self.triggered = False
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

    def __str__(self):
        if self.filename is None:
            return f"NoFile-{self.freq}-{self.duration}"
        else:
            return f"{self.filename}-{self.freq}-{self.duration}"

    def callback(self, recognizer, audio):
        try:
            if self.trigger_word in recognizer.recognize_sphinx(audio):
                print("Trigger!")
                self.trigger = True
            else:
                print(recognizer.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Sphinx; {0}".format(e))

    def listen_sphinx(self):
        with self.m as source:
            audio = self.r.listen(source)

        try:
            if self.trigger_word in self.r.recognize_sphinx(audio):
                print("Trigger!")
                self.triggered = True
            else:
                print(self.r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Sphinx; {0}".format(e))

    def listen_whisper(self):
        client = OpenAI()

        audio_file = open("/path/to/file/audio.mp3", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        print(transcription.text)

    def wait_for_trigger(self):
        while self.triggered is False:
            self.listen_sphinx()


