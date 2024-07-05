import datetime
from judylog.judylog import judylog
from api.openaiapi import openAIGPT
from api.promptcreate import promptCreate


class dailySummary:
    '''
    Contains the daily summary information based.
    '''

    def __init__(self, chat_history, date):
        self.date = date.date()  # Accepts datetime input and converts to date
        self.summary_info = {
            'sentiment': None,
            'summary': None,
            'conv_count': 0,
            'exch_count': 0,
            'keywords': [],
            'date': self.date
        }
        self.conv_list = {
            'ids': [],
            'data': []
        }
        self.exch_list = []

        judylog.info(f'dailySummary.__init__ > Creating daily summary for {self.date}')

        # Gather all conversations from the date
        for conv in chat_history.conversations:
            if conv.date.date() == self.date:
                self.conv_list['data'].append(conv)
                self.conv_list['ids'].append(conv.id)
                self.summary_info['conv_count'] += 1

        print(f'Total conversations: {self.summary_info['conv_count']}')

        # Gather the exchanges associated with the conversations
        for exch in chat_history.exchanges:
            if exch.conv_id in self.conv_list['ids']:
                self.summary_info['exch_count'] += 1
                self.exch_list.append(exch)

        print(f'Total exchanges: {self.summary_info['exch_count']}')

        # Determine the overall sentiment
        api_call = openAIGPT()
        api_response = api_call.get_summ_info(self.exch_list)
        self.summary_info['summary'] = api_response['summary']
        self.summary_info['keywords'] = api_response['keywords']
        self.summary_info['sentiment'] = api_response['sentiment']

        print(self.summary_info)

        # Save and ensure the watchers and caretaker fields are accurate


if __name__ == '__main__':
    from data_mgmt.chat.chat_history import chatHistory
    from user_credentials import get_user_credentials
    from maint.patient_settings import patientSettings

    email, password = get_user_credentials('Colin Raymond')
    credentials = {
        'email': email,
        'password': password,
        'patient_id': None,
        'api_token': None
    }

    # Need to set settings
    settings = {
        'photo_delay': '4',
        'accent': 'American',
        'trigger': 'Judy'
    }
    patient_settings = patientSettings(credentials)
    patient_settings.pull_settings()

    # Get data from Bubble
    chat_history = chatHistory(settings, credentials)
    chat_history.import_data()

    summary = dailySummary(chat_history, datetime.datetime(year=2024, day=4, month=7))

