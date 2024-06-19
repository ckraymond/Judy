'''
Main class that runs the voice prompts on Judy.
'''

import speech_recognition as sr
import logging

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
        logging.info('Starting to listen through microphone.')

        while True:
            with self.m as source:
                audio_data = self.r.listen(source)
                text = self.r.recognize_google(audio_data)
                print(text)

            if self.KEYWORD in text:
                self.request_response()

    def request_response(self):

