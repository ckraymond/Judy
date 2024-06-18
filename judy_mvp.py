from photo_display.slideshow import slideShow        # Used to actually display the photos
from data_mgmt.chat.chat_history import chatHistory
from data_mgmt.patient.patient_info import patientInfo

class judyMVP:

    def __init__(self, judylog):
        '''
        Initialization function for Judy. Actions taken:
        1.) Download files from Bubble.
        2a.) Initilize the photo carousel
        2b.) Start listening on the microphone
        3.) Regular maintenance routine to pull down info from Bubble
        '''

        # First, we will pull down the file system from Bubble
        self.chat_history = chatHistory()  # Creates the chat history and loads from the history file
        self.chat_history.import_data()

        self.patient_info = patientInfo()  # Gets the patient's information
        self.patient_info.import_data()

        photo_slideshow = slideShow()
