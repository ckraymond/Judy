import datetime
from judylog.judylog import judylog
from api.openaiapi import openAIGPT
from api.bubbleapi import bubbleAPI

class dailySummary:
    '''
    Creates the daily summary information based on the information provided to it around exchanges and conversations.
    '''

    def __init__(self, chat_history, date: datetime.datetime, bubble_creds):
        self.summary_info = {
            'id': None,
            'sentiment': None,
            'summary': None,
            'conv_count': 0,
            'exch_count': 0,
            'keywords': [],
            'date': date,
            'patient_id': bubble_creds['patient_id'],
            'caretaker_id': bubble_creds['caretaker_id'],
            'watcher_ids': bubble_creds['watcher_ids']
        }
        self.conv_list = {
            'ids': [],
            'data': []
        }
        self.exch_list = []

        # First we need to check and make sure that there is not already something in Bubble
        if self.summary_info['date'] != date.today():
            bubble_api = bubbleAPI(bubble_creds)
            api_result =  bubble_api.check_for_summ(self.summary_info['date'])
        else:
            api_result = {'response': {}}

        if '_id' in api_result['response']['results'].keys():
            self.save_from_bubble(api_result['response']['results'])

        else:
            judylog.info(f'dailySummary.__init__ > Creating daily summary for {self.summary_info['date']}')

            # Gather all conversations from the date
            for conv in chat_history.conversations:
                if conv.date.date() == self.summary_info['date']:
                    self.conv_list['data'].append(conv)
                    self.conv_list['ids'].append(conv.id)
                    self.summary_info['conv_count'] += 1

            # Gather the exchanges associated with the conversations
            for exch in chat_history.exchanges:
                if exch.conv_id in self.conv_list['ids']:
                    self.summary_info['exch_count'] += 1
                    self.exch_list.append(exch)

            # Determine the overall sentiment
            if self.summary_info['exch_count'] > 0:
                api_call = openAIGPT()
                api_response = api_call.get_summ_info(self.exch_list)
                self.summary_info['summary'] = api_response['summary']
                self.summary_info['keywords'] = api_response['keywords']
                self.summary_info['sentiment'] = api_response['sentiment']
            else:
                self.summary_info['summary'] = 'None'
                self.summary_info['keywords'] = 'None'
                self.summary_info['sentiment'] = 'N/A'

            self.save_summary(bubble_creds)

    def save_summary(self, bubble_creds):
        # Check to see if there is already a summary there so we don't overwrite
        bubble_api = bubbleAPI(bubble_creds)
        result =  bubble_api.check_for_summ(self.summary_info['date'])

        if '_id' not in result['response'].keys():
            # Save and ensure the watchers and caretaker fields are accurate
            api_response = bubble_api.save_daily_summary(self.summary_info)
            self.summary_info['id'] = api_response['response']['_id']
        elif self.summary_info['date'] == datetime.date.today():
            pass

    def save_from_bubble(self, response):
        self.summary_info['id'] = response['_id']
        self.summary_info['sentiment'] = response['sentiment']
        self.summary_info['summary'] = response['summary']
        self.summary_info['conv_count'] = response['chat_count']
        self.summary_info['exch_count'] = response['exchange_count']
        self.summary_info['date'] = self.convert_date(response['date'])
        self.summary_info['patient_id'] = response['patient']
        self.summary_info['watcher_ids'] = response['watcher']
        self.summary_info['caretaker_id'] = response['caretaker']
        self.summary_info['keywords'] = self.convert_kwds(response['keywords'])

    @staticmethod
    def convert_kwds(old_keywords):
        new_keywords = []
        for keyword in old_keywords:
            new_keyword = {}

            #Parse whats in there to pull out the count and keyword
            if keyword.find("(") >= 0:
                keyword_key = keyword[0:keyword.find("(")-1]
                count = int(keyword[keyword.find("(")+1:keyword.find(")")])
            else:
                keyword_key = keyword
                count = 1

            new_keyword[keyword_key] = count
            new_keywords.append(new_keyword)
        return new_keywords

    @staticmethod
    def convert_date(timestamp):
        return_date = datetime.date.fromtimestamp(timestamp/1000)
        return return_date

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

    patient_settings = patientSettings(credentials)
    patient_settings.pull_settings()

    # Get data from Bubble
    chat_history = chatHistory(patient_settings.values, credentials)
    chat_history.import_data()

    summary = dailySummary(chat_history, datetime.datetime(year=2024, day=4, month=7), credentials)
    summary.save_summary(credentials)

    # keyword_strings = ['Luciane (2)', 'family (2)', 'birthday (1)', 'gift ideas (1)', '4th of July fireworks (1)']
    # print(dailySummary.convert_kwds(keyword_strings))
    #
    # date_utc = 1720065600000
    # print(dailySummary.convert_date(date_utc))

