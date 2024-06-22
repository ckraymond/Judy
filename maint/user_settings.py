from api.bubbleapi import bubbleAPI
from judylog.judylog import judylog
class userSettings:
    '''
    Stores and adjusts all device and user settings.
    '''
    def __init__(self):
        self.settings = {
            'photo_delay': '',
            'accent': '',
            'trigger': ''
        }

    def pull_settings(self):
        '''
        Pull settings from Bubble and update.
        TODO: Need to be able to share the settings across the various threads
        :return:
        '''
        api_connection = bubbleAPI()
        api_results = api_connection.get_records('settings')

        self.settings['accent'] = api_results[0]['accent']
        self.settings['photo_delay'] = int(api_results[0]['photo_delay'])
        self.settings['trigger'] = api_results[0]['trigger']

        judylog.info(f'userSettings.pull_settings > Imported settings: {self.settings}')

        return True