import PySimpleGUI as sg                    # Base function for the simple GUI
import pygame
from gtts import gTTS
import logging

from data_mgmt.chat_history import chatHistory, chatExchange       # Class that stores the chat exchance
from api.openaiapi import openai_api_call     # Class that handles querying the OpenAI API
from soundprocessing import soundProcessing
from init.judyparams import GUI_PARAMS


class judyGUI:
    # Class to support the GUI for judy.

    def __init__(self):
        '''
        Initializes the relatively simple GUI and waits for user instruction.
        '''
        # TODO: Adjust dimensions to pull screen size and do a percentage
        self.chat_history = chatHistory()           # Creates the chat history and loads from the history file

        self.layout = [[sg.Push(), sg.Image('./data/judy_circle.png', subsample=5), sg.Push()],
                       [sg.Push(), sg.Button('Ask Question', bind_return_key=True), sg.Button('Quit'), sg.Push()]]

        self.window = sg.Window(GUI_PARAMS['title'],
                                self.layout,
                                size=(GUI_PARAMS['x_size'], GUI_PARAMS['y_size']),
                                resizable=True)

        logging.info('Judy GUI Initialized.')
        print('Judy GUI Initialized')

    def window_read(self):
        '''
        Function loops through until user clicks quit
        :return:
        '''

        while True:
            self.event, self.values = self.window.read()

            if self.event in ('Quit', None, sg.WIN_CLOSED):
                break
            elif self.event == 'Ask Question':
                self.submit_question()

    def submit_question(self):
        new_exchange = chatExchange()
        new_exchange.query = self.ask_question()
        new_exchange.response = openai_api_call(new_exchange.query, self.chat_history.exchanges)          # Reaches out to the API and submits the question
        self.chat_history.exchanges.append(new_exchange)
        new_exchange.post_exch()                                                    # Saves the exchange onto Bubble
        self.read_response(new_exchange.response)

    def ask_question(self):
        self.ask_layout = [[sg.Push()],[sg.Image('Judy.jpeg'),[sg.Push()]]]
        self.ask_window = sg.Window('Ask Your Question',
                                    self.ask_layout,
                                    size=(100, 100),
                                    resizable=True)
        recording = soundProcessing()
        query = recording.get_query()
        return query

    def read_response(self, response):
        language = 'en'
        myobj = gTTS(text = response, lang = 'en', slow=False)
        myobj.save('./temp/response.mp3')

        # Initialize the mixer module
        pygame.mixer.init()

        # Load the mp3 file
        pygame.mixer.music.load('./temp/response.mp3')

        # Play the loaded mp3 file
        pygame.mixer.music.play()
