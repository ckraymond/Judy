from judylog.judylog import judylog
from maint.patient_settings import patientSettings
from datetime import datetime, timedelta, date
from data_mgmt.summaries.weekly_summary import weeklySummary
import time
class judyMaint:
    '''
    Intended to run in the background and continually checking to see if there are any updates to the program.

    Specific actions are:
    - Update the exchanges.
    - Update the conversations.
    - Check for any new photos
    - Update the user preferences
    '''

    def __init__(self, bubble_creds):
        # On initialization, get user settings
        self.bubble_creds = bubble_creds
        self.settings = patientSettings(self.bubble_creds)
        self.settings.pull_settings()

    def run_background(self, chat_history, message_handler):
        '''
        Routine to run in the background and keep the device updated. Routine includes:
        - Checking settings
        - Validating exchanges
        - Validating conversations
        - Checking photos
        - Prompting user occaissionally
        :return:
        '''
        print('judyMaint.run_background > Running maintenance routine')

        while True:
            time.sleep(60)                                                      # Only runs every min to save processing
            if datetime.now().hour % 12 == 0 and datetime.now().minute == 0:    # Runs once a day
                weeklySummary(date.today() - timedelta(days=1), chat_history, self.bubble_creds)
            if datetime.now().minute % 5 == 0:                                  # Certain ones only run every 5 min
                judylog.info(f'judyMaint.run_background > Running maintenance routine')
                self.settings.pull_settings()

                # Go through and clean up conversations and exchanges
                chat_history.clean_exchanges()
                chat_history.check_mappings()
                chat_history.clean_conversations()
                chat_history.rev_conversations()
                chat_history.save_history()
                chat_history.remove_orph_convos()

            # Check to see if there are any messages on Bubble
            message_handler.get_messages()
            message_handler.clean_messages()
            message_handler.alert_messages()


