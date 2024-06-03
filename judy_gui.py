import PySimpleGUI as sg                    # Base function for the simple GUI
import pygame
from gtts import gTTS

from chat_history import chatHistory       # Class that stores the chat exchance
from api_integration import openai_api_call     # Class that handles querying the OpenAI API
from judyparams import *
from soundprocessing import soundProcessing

import time
class judyGUI:
    # Class to support the GUI for judy.

    def __init__(self):
        self.params = {
            'theme': 'LightBlue2', # List can be found through sg.theme_previewer() or .list() functions
            'x_size': 900,
            'y_size': 400,
            'title': 'Judy v0.01',
            'chat_fn': 'chat_history.dat',
            'chat_history': ''
        }
        # TODO: Adjust dimensions to pull screen size and do a percentage
        self.chat_history = chatHistory()           # Creates the chat history and loads from the history file
        self.create_history_string()

        # Enact options for the window
        sg.theme(self.params['theme'])

        # Set the variables for the input and output
        # self.input = sg.Input(key='input', expand_x=True, expand_y=True)
        self.output = sg.Multiline(self.params['chat_history'], key='output', size=(700, 15), expand_x=True, expand_y=True)

        self.layout = [[sg.Push(), self.output, sg.Push()],
                  [sg.Push(), sg.Button('Ask Question', bind_return_key=True), sg.Button('Quit'), sg.Push()]]

        self.window = sg.Window(self.params['title'],
                                self.layout,
                                size=(self.params['x_size'], self.params['y_size']),
                                resizable=True)

    def window_read(self):
        # Class to await user input on the window

        while True:
            self.event, self.values = self.window.read()

            if self.event in ('Quit', None, sg.WIN_CLOSED):
                break
            elif self.event == 'Ask Question':
                self.submit_question()

    def submit_question(self):
        query = self.ask_question()
        response = openai_api_call(query)                   # Reaches out to the API and submits the question
        self.chat_history.append(query, response)           # Updates the chat history and saves (eventually)
        self.chat_history.assign_ids()                      # Sets the conversation IDs

        self.create_history_string()
        self.window['output'].update(self.params['chat_history'])

        self.read_response(response)

    def ask_question(self):
        self.ask_layout = [[sg.Push()],[sg.Image('Judy.jpeg'),[sg.Push()]]]
        self.ask_window = sg.Window('Ask Your Question',
                                    self.ask_layout,
                                    size=(100, 100),
                                    resizable=True)
        recording = soundProcessing()
        query = recording.get_query()
        return query

    def create_history_string(self):
        # Default welcome
        self.params['chat_history'] = ''
        item = len(self.chat_history.history)-1

        while item >= 0:
            new_exchange = '\nQuestion: ' + self.chat_history.history[item].query + '\n\n' + 'Response: ' + self.chat_history.history[item].response + '\n' + '-' * 20 + '\n'
            self.params['chat_history'] += new_exchange
            item -= 1

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
