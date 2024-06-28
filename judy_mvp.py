from photo_display.slideshow import slideShow        # Used to actually display the photos
from data_mgmt.chat.chat_history import chatHistory
from data_mgmt.patient.patient_info import patientInfo
from voice.judy_voice import judyVoice
from judylog.judylog import judylog
from maint.judy_maint import judyMaint
from maint.messages import messageHandler
from api.bubbleapi import bubbleAPI

import threading

class judyMVP:

    def __init__(self, is_mac, mac_choice, dev_mode, email, password):
        '''
        Initialization function for Judy. Actions taken:
        1.) Download files from Bubble.
        2a.) Initialize the photo carousel
        2b.) Start listening on the microphone
        3.) Regular maintenance routine to pull down info from Bubble
        '''

        # These credentials will be used throughout the model
        self.bubble_creds = {
            'email': email,
            'password': password,
            'patient_id': None,
            'api_token': None,
            'caretaker_id': None,
            'watcher_ids': []
        }

        judylog.info('judyMVP.__init__ > Initializing the program.')
        self.dev_mode = dev_mode                # Check on dev mode aspect
        self.maint = judyMaint(self.bubble_creds)      # Pull the user settings

        # First, we will pull down the file system from Bubble
        self.chat_history = chatHistory(self.maint.settings.values, self.bubble_creds)  # Creates the chat history and loads from the history file
        self.chat_history.import_data()

        self.patient_info = patientInfo(self.bubble_creds)  # Gets the patient's information
        self.patient_info.import_data()

        self.message_handler = messageHandler(self.bubble_creds)

        if is_mac is not True and self.dev_mode is False:
            # THIS IS THE MULTITHREADING WE WILL RUN LATER
            self.t_slideshow = threading.Thread(target = self.start_slideshow)
            self.t_audio = threading.Thread(target = self.start_audio)
            self.t_maint = threading.Thread(target = self.start_maint)

            self.t_slideshow.start()
            self.t_audio.start()
            self.t_maint.start()

            self.t_slideshow.join()
            self.t_audio.join()
            self.t_maint.join()

        # Support for mac developer mode
        else:
            if mac_choice == '1':
                self.start_slideshow()
            elif mac_choice == '2':
                self.start_audio()
            elif mac_choice == '3':
                self.start_maint()
            else:
                print('Choice not recognized.')

    def start_slideshow(self):
        judylog.info('judyMVP.__init__ > Starting slideshow thread.')
        photo_slideshow = slideShow(self.maint.settings.values, self.bubble_creds)

    def start_audio(self):
        judylog.info('judyMVP.__init__ > Starting audio thread.')
        voice = judyVoice(self.maint.settings.values, self.bubble_creds, self.dev_mode)
        voice.listen(self.chat_history, self.patient_info)

    def start_maint(self):
        judylog.info('judyMVP.__init__ > Starting maintenance thread.')
        self.maint.run_background(self.chat_history, self.message_handler)