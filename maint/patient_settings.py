from api.bubbleapi import bubbleAPI
from judylog.judylog import judylog
class patientSettings:
    '''
    Stores and adjusts all device and user settings.
    '''
    def __init__(self, patient_id):
        self.values = {
            'photo_delay': '',
            'accent': '',
            'trigger': ''
        }

        self.patient_id = patient_id            # This will be used for all queries going forward

    def pull_settings(self):
        '''
        Pull settings from Bubble and update.
        TODO: Need to be able to share the settings across the various threads
        :return:
        '''
        api_connection = bubbleAPI(self.patient_id)
        api_results = api_connection.get_records('settings')

        try:
            self.values['accent'] = api_results[0]['accent']
        except:
            judylog.error(f'patientSettings.pull_settings > Unable to load accent. Using default instead.')
            self.values['accent'] = 'american'

        try:
            self.values['photo_delay'] = int(api_results[0]['photo_delay'])
        except:
            judylog.error(f'patientSettings.pull_settings > Unable to load photo_delay. Using default instead.')
            self.values['photo_delay'] = 5

        try:
            self.values['trigger'] = api_results[0]['trigger']
        except:
            judylog.error(f'patientSettings.pull_settings > Unable to load trigger_phrase. Using default instead.')
            self.values['trigger'] = 'judy'

        judylog.info(f'userSettings.pull_settings > Imported settings: {self.values}')

        return True