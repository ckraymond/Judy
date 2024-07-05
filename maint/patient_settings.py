from api.bubbleapi import bubbleAPI
from judylog.judylog import judylog
class patientSettings:
    '''
    Stores and adjusts all device and user settings.
    '''
    def __init__(self, bubble_creds):
        self.values = {
            'photo_delay': '',
            'accent': '',
            'trigger': ''
        }

        self.bubble_creds = bubble_creds           # This will be used for all queries going forward

    def pull_settings(self):
        '''
        Pull settings from Bubble and update.
        TODO: Need to be able to share the settings across the various threads
        :return:
        '''
        api_connection = bubbleAPI(self.bubble_creds)
        api_results = api_connection.get_settings()

        try:
            self.values['accent'] = api_results['accent']
        except:
            judylog.error(f'patientSettings.pull_settings > Unable to load accent. Using default instead.')
            self.values['accent'] = 'american'

        try:
            self.values['photo_delay'] = api_results['photo_delay']
        except:
            judylog.error(f'patientSettings.pull_settings > Unable to load photo_delay. Using default instead.')
            self.values['photo_delay'] = 5

        try:
            self.values['trigger'] = api_results['trigger']
        except:
            judylog.error(f'patientSettings.pull_settings > Unable to load trigger_phrase. Using default instead.')
            self.values['trigger'] = 'judy'

        #TODO: These last two pull from settings but the source of truth is the patient's user record
        self.bubble_creds['caretaker_id'] = api_results['caretaker']
        try:
            self.bubble_creds['watcher_ids'] = api_results['watcher']
        except:
            judylog.error(f'patientSettings.pull_settings > Unable to load any watchers.')
            self.bubble_creds['watcher_ids'] = []

        judylog.info(f'userSettings.pull_settings > Imported settings: {self.values}')

        return True