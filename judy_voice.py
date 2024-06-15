'''
Main class that runs the voice prompts on Judy.
'''

import speech_recognition as sr
import judylog

class judyVoice:

    def __init__(self):
        # obtain audio from the microphone
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.KEYWORD = 'judy'

        # Adjust for the ambient noise
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    def listen(self):
        '''
        Simple listener that just waits to hear if the keyword is spoken
        :return:
        '''
        judylog.info('Starting to listen through microphone.')

        while True:
            with self.m as source:
                audio_data = self.r.listen(source)
                text = self.r.recognize_google(audio_data)
                print(text)

            if self.KEYWORD in text:
                break

        # with sr.Microphone() as source:
        #     print("Say something!")
        #     audio = r.listen(source)
        #
        # # Using Google edge voice processing
        # try:
        #     # for testing purposes, we're just using the default API key
        #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        #     # instead of `r.recognize_google(audio)`
        #     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        # except sr.UnknownValueError:
        #     print("Google Speech Recognition could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
