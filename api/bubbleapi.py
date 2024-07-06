import requests         # For the call
from datetime import timedelta, datetime

from judylog.judylog import judylog

class bubbleAPI:
    def __init__(self, credentials):
        self.base_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/obj'
        self.wf_url = 'https://colinkraymond.bubbleapps.io/version-test/api/1.1/wf'
        self.credentials = credentials

    def get_token(self):
        '''
        Uses the users login and password to get a token for API calls.
        :return:
        '''
        call_url = f'{self.wf_url}/gen_api_token?email={self.credentials['email']}&pw={self.credentials['password']}'

        response = requests.get(call_url).json()
        judylog.info(f'bubbleAPI.get_token > Getting new API key using credentials for {self.credentials['email']}')

        self.credentials['api_token'] = response['response']['token']
        self.credentials['patient_id'] = response['response']['user_id']

    def check_response(self, response):
        '''
        Checks the JSON formed response and validates that the response was successfull. If not, returns the status.
        :param response:
        :return:
        '''

        if 'error_class' in response.keys():
            if response['error_class'] == 'Unauthorized' and response['translation'] == 'Invalid or expired token: None':
                return 'invalid_token'
        elif 'statusCode' in response.keys():
            if response['statusCode'] == 404:
                return 'data_type_not_found'
        else:
            return 'success'

    def get_exch_conv(self, type):
        '''
                Requests to get record of a certain type from Bubble.
                :param type:
                :return:
                '''
        recds_remaining = 1  # Set this to 1 to start
        cursor = 0
        limit = 100  # This will remain the same through all the calls
        response_list = []
        judylog.info(f'bubbleAPI.get_exch_conv > Getting, {type}, records from Bubble.')

        # Type should be in chatexchange or conversation
        allowed_types = ['conversation', 'chatexchange', 'user', 'friends', 'interest', 'photo', 'faq', 'message']
        if type not in allowed_types:
            raise ValueError(f'bubbleAPI.get_exch_conv > Type should be one of: {', '.join(allowed_types)}.')

        while recds_remaining > 0:
            call_url = f'{self.base_url}/{type}?cursor={cursor}&limit={limit}'
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.get(call_url, headers=head).json()

            # If call unsuccessful get a new token and try again
            if self.check_response(response) == 'invalid_token':
                # Try and get the token and then make the call again
                self.get_token()
                head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
                response = requests.get(call_url, headers=head).json()

            # Add the records into the response list and move the cursor to paganate
            response_list.extend(response['response']['results'])
            recds_remaining = response['response']['remaining']
            cursor += limit

        judylog.info(f'bubbleAPI.get_records > {response_list[0:5]}')
        judylog.info(f'bubbleAPI.get_records > Total {type} records pulled: {len(response_list)}')
        return response_list

    def get_settings(self):
        '''
        Used to get the patient's settings from Bubble.
        :return:
        '''

        judylog.info(f'bubbleAPI.get_settings > Getting patient and device settings from Bubble.')

        call_url = f'{self.base_url}/setting?'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        response = requests.get(call_url, headers=head).json()
        judylog.info(f'bubbleAPI.get_settings > response: {str(response)[0:100]}')

        # If call unsuccessful get a new token and try again
        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.get(call_url, headers=head).json()

        judylog.info(f'bubbleAPI.get_settings > {str(response)}')
        return response['response']['results'][0]

    def update_conv_rcds(self, conv):
        '''
        Updates a conversation record in Judy.
        :param conv:
        :return:
        '''
        judylog.info(f'bubbleAPI.update_conv_rcds > Updating conversation (ID: {conv.id}) to Bubble.')
        call_url = self.wf_url + '/' + 'put_conversation'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            'date': str(conv.date),
            'summary': conv.summary,
            'sentiment': conv.sentiment,
            'keywords': ','.join(conv.keywords),
            'id': conv.id
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.get(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'bubbleAPI.update_conv_rcds > Unable to update id in Bubble: {body['id']}')
            judylog.error(f'bubbleAPI.update_conv_rcds > {response}')
            return False

    def post_record(self, type, body):
        '''
        Posts a record of type to Bubble
        :param type:
        :param body:
        :return:
        '''
        judylog.info(f'bubbleAPI.post_record > Posting {type} record to Bubble.')
        post_url = self.base_url + '/' + type
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}

        body['patient'] = self.credentials['patient_id']
        body['caretaker'] = self.credentials['caretaker_id']
        body['watcher'] = self.credentials['watcher_ids']

        response = requests.post(post_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(post_url, headers=head, json=body).json()

        judylog.info(f'bubbleAPI.post_record > Response: {response}')
        return response

    def update_exch_rcds(self, exchange):
        judylog.info(f'bubbleAPI.update_exch_rcds > Updating exchange (ID: {exchange.id}) to Bubble.')
        call_url = self.wf_url + '/' + 'put_exchange'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            'date': str(exchange.date),
            'query': exchange.query,
            'response': exchange.response,
            'summary': exchange.summary,
            'id': exchange.id,
            'conv_id': exchange.conv_id,
            'patient': self.credentials['patient_id'],
            'caretaker': self.credentials['caretaker_id'],
            'watcher': self.credentials['watcher_ids']
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'Unable to update exchange id in Bubble: {body['id']}')
            judylog.error(response)
            return False
    #TODO: Need to add in error handling for when something doesn't work

    def remove_recd(self, type, id):
        '''
        Takes an ID, connects to the bubble API and then removes it from Bubble.
        :return:
        '''

        judylog.info(f'bubbleAPI.remove_recd > Removing record (ID: {id}) from Bubble with workflow {type}.')
        call_url = f'{self.wf_url}/{type}'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            'id': id
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'bubbleAPI.remove_recd > Unable to remove id in Bubble: {body['id']}')
            judylog.error(response)
            return False

    def save_daily_summary(self, summary_info):
        '''
        Takes the daily summary information and saves onto bubble.
        :param summary_info:
        :return:
        '''

        judylog.info(f'bubbleAPI.save_daily_summary > Updating daily summary (ID: {summary_info['id']}) to Bubble.')
        call_url = self.wf_url + '/' + 'save_daily_summ'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            '_id': summary_info['id'],
            'date': self.conv_date(summary_info['date']),
            'summary': summary_info['summary'],
            'sentiment': summary_info['sentiment'],
            'keywords': self.conv_keywords(summary_info['keywords']),
            'exch_count': summary_info['exch_count'],
            'conv_count': summary_info['conv_count'],
            'patient': summary_info['patient_id'],
            'caretaker': summary_info['caretaker_id'],
            'watcher': summary_info['watcher_ids']
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'Unable to update exchange id in Bubble: {body['id']}')
            judylog.error(response)
            return False

    def check_for_summ(self, date):
        '''
        Checks to see if there is already a summary present and if so, it returns the id
        :param date:
        :return:
        '''

        judylog.info(f'bubbleAPI.check_for_summ > Checking Bubble for summary on {date}.')
        call_url = self.wf_url + '/' + 'check_for_summ'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {'date': self.conv_date(date)}

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'Unable to update exchange id in Bubble: {body['id']}')
            judylog.error(response)
            return False

    def save_weekly_summ(self, weekly_summ):
        judylog.info(f'bubbleAPI.save_daily_summary > Updating weekly summary (ID: {weekly_summ['id']}) to Bubble.')
        call_url = self.wf_url + '/' + 'save_weekly_summ'
        head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
        body = {
            'start_date': self.conv_date(weekly_summ['start_date']),
            'end_date': self.conv_date(weekly_summ['end_date']),
            'summary': weekly_summ['summary'],
            'sentiment': weekly_summ['sentiment'],
            'keywords': self.conv_keywords(weekly_summ['keywords']),
            'exch_count': weekly_summ['exch_count'],
            'conv_count': weekly_summ['conv_count'],
            'daily_summ_ids': weekly_summ['daily_summ_ids'],
            'patient': self.credentials['patient_id'],
            'caretaker': self.credentials['caretaker_id'],
            'watcher': self.credentials['watcher_ids']
        }

        response = requests.post(call_url, headers=head, json=body).json()

        if self.check_response(response) == 'invalid_token':
            # Try and get the token and then make the call again
            self.get_token()
            head = {'Authorization': 'token {}'.format(self.credentials['api_token'])}
            response = requests.post(call_url, headers=head, json=body).json()

        if response['status'] == 'success':
            return response
        else:
            judylog.error(f'Unable to update exchange id in Bubble: {body['id']}')
            judylog.error(response)
            return False

    @staticmethod
    def conv_keywords(kywd_tuple):
        ret_list = []
        for tuple in kywd_tuple:
            line_str = f'{list(tuple.keys())[0]} ({list(tuple.values())[0]})'
            ret_list.append(line_str)
        return ret_list

    @staticmethod
    def conv_date(old_date):
        new_date = datetime.combine(date = old_date, time=datetime.min.time())
        new_date += timedelta(hours = 4)

        return str(new_date)




if __name__ == '__main__':
    # Get the user credentials that we will use to log in to various things
    from user_credentials import get_user_credentials
    email, password = get_user_credentials('Donald Trump')
    credentials = {
        'email': email,
        'password': password,
        'patient_id': None,
        'api_token': None
    }

    test = bubbleAPI(credentials)
    users = test.get_exch_conv('interest')
    for user in users:
        print(user)