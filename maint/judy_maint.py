from api.bubbleapi import bubbleAPI
from maint.user_settings import userSettings
import time
class judyMaint():
    '''
    Intended to run in the background and continually checking to see if there are any updates to the program.

    Specific actions are:
    - Update the exchanges.
    - Update the conversations.
    - Check for any new photos
    - Update the user preferences
    '''

    def __init__(self):
        self.settings = userSettings()
        self.settings.pull_settings()

    def run_background(self):
        '''
        Routine to run in the background and keep the device updated. Routine includes:
        - Checking settings
        - Validating exchanges
        - Validating conversations
        - Checking photos
        - Prompting user occaissionally
        :return:
        '''

        self.settings.pull_settings()

        time.sleep(300)                         #Only runs every 5 min to save processing