from photo_display.slideshow import slideShow        # Used to actually display the photos
from data_mgmt.chat.chat_history import chatHistory
from data_mgmt.patient.patient_info import patientInfo
from voice.judy_voice import judyVoice
from judylog.judylog import judylog

import threading

class judyMVP:

    def __init__(self, dev_mode, is_mac, mac_choice):
        '''
        Initialization function for Judy. Actions taken:
        1.) Download files from Bubble.
        2a.) Initilize the photo carousel
        2b.) Start listening on the microphone
        3.) Regular maintenance routine to pull down info from Bubble
        '''

        judylog.info('judyMVP.__init__ > Initializing the program.')

        # First, we will pull down the file system from Bubble
        self.chat_history = chatHistory()  # Creates the chat history and loads from the history file
        self.chat_history.import_data()

        self.patient_info = patientInfo()  # Gets the patient's information
        self.patient_info.import_data()

        if is_mac is not True:
            # THIS IS THE MULTITHREADING WE WILL RUN LATER
            self.t_slideshow = threading.Thread(target = self.start_slideshow)
            self.t_audio = threading.Thread(target = self.start_audio)

            self.t_slideshow.start()
            self.t_audio.start()

            self.t_slideshow.join()
            self.t_audio.join()

        else:
            if mac_choice == '1':
                self.start_slideshow()
            elif mac_choice == '2':
                self.start_audio()
            else:
                print('Choice not recognized.')

    def start_slideshow(self):
        photo_slideshow = slideShow()

    def start_audio(self):
        voice = judyVoice()
        voice.listen(self.chat_history, self.patient_info)