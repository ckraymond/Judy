from .daily_summary import dailySummary
from api.openaiapi import openAIGPT
from api.bubbleapi import bubbleAPI
from datetime import timedelta

class weeklySummary:

    def __init__(self, end_date, chat_history, bubble_creds):
        '''
        Initilization to create the weekly summary. Will take a seven day period rather than a specific week.
        So really is a last seven day summary.
        '''
        self.date_info = []
        self.summary_info = {
            'id': None,
            'summary': 'None',
            'keywords': 'None',
            'sentiment': 'N/A',
            'exch_count': 0,
            'conv_count': 0,
            'start_date': None,
            'end_date': end_date,
            'daily_summ_ids': []
        }

        self.create_date_struct(chat_history, bubble_creds)
        self.update_overall_summary()
        self.save_summary(bubble_creds)

    def create_date_struct(self, chat_history, bubble_creds):
        '''
        Creates the overall framework for the date structure list.
        :param end_date:
        :return:
        '''
        self.date_info = []
        single_date = self.summary_info['end_date'] - timedelta(6)
        self.summary_info['start_date'] = self.summary_info['end_date'] - timedelta(6)

        while single_date <= self.summary_info['end_date']:
            day_obj = dailySummary(chat_history, single_date, bubble_creds)
            self.date_info.append(day_obj)

            self.summary_info['exch_count'] += day_obj.summary_info['exch_count']
            self.summary_info['conv_count'] += day_obj.summary_info['conv_count']
            single_date += timedelta(1)

    def update_overall_summary(self):
        '''
        Takes the overall information and sends to ChatGPT to analyze summary, keywords, and other information.
        :param chat_history:
        :return:
        '''

        if self.summary_info['exch_count'] > 0:
            api_connection = openAIGPT()
            api_response = api_connection.gen_weekly_summary(self.date_info)

            self.summary_info['summary'] = api_response['summary']
            self.summary_info['keywords'] = api_response['keywords']
            self.summary_info['sentiment'] = api_response['sentiment']

    def save_summary(self, bubble_creds):
        '''
        Saves the weekly summary onto Bubble.
        :return:
        '''

        self.summary_info['daily_summ_ids'] = []

        for summ in self.date_info:
            self.summary_info['daily_summ_ids'].append(summ.summary_info['id'])

        bubble_api = bubbleAPI(bubble_creds)
        bubble_api.save_weekly_summ(self.summary_info)


if __name__ == '__main__':
    from datetime import date, timedelta
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
    chat_history = chatHistory(patient_settings.values, credentials)
    chat_history.import_data()

    test = weeklySummary(date.today()-timedelta(days = 1), chat_history, credentials)