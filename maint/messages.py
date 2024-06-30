from api.bubbleapi import bubbleAPI
from judylog.judylog import judylog
from voice.judy_voice import judyVoice
import datetime

class messageHandler:
    def __init__(self, credentials, settings):
        self.messages = []
        self.bubble_creds = credentials
        self.settings = settings

    def get_messages(self):
        '''
        Routine to check and see if there are messages waiting on Bubble
        :return:
        '''

        # Pull the raw list of messages from Bubble
        judylog.info(f'messageHandler.clean_messages > Checking for messages on Bubble')
        api_connection = bubbleAPI(self.bubble_creds)
        new_messages = api_connection.get_exch_conv('message')

        for msg in new_messages:
            self.check_msg_fields(msg)

            # Creates and array with each of the alert triggers
            msg['Alert Triggers'] = []
            trig_time = datetime.datetime.now()
            while trig_time < msg['Expiration Date']:
                msg['Alert Triggers'].append(trig_time)
                trig_time += datetime.timedelta(minutes = msg['Frequency'])

        if len(self.messages) == 0:
            self.messages = new_messages

        else:
            id_list = []
            for message in self.messages:
                id_list.append(message['_id'])

            for index in range(len(new_messages)):
                if new_messages[index]['_id'] not in id_list:
                    self.messages.append(new_messages[index])

    def clean_messages(self):
        '''
        Goes through the messages and determines if there are any that need to be deleted
        :return:
        '''

        judylog.info(f'messageHandler.clean_messages > Cleaning messages')

        for msg in range(len(self.messages)-1, -1, -1):
            if self.messages[msg]['Expiration Date'] < datetime.datetime.now():
                judylog.info(f'messageHandler.clean_messages > Deleting message: {msg}')
                del_msg = self.messages.pop(msg)

                api_connection = bubbleAPI(self.bubble_creds)
                print(api_connection.remove_recd('del_message', del_msg['_id']))
                judylog.info(f'messageHandler.clean_message > {api_connection.remove_recd('del_message', del_msg['_id'])}')

    def alert_messages(self):
        '''
        Goes through the messages and alerts user if any of the frequency thresholds have been hit
        :return:
        '''

        judylog.info(f'messageHandler.clean_messages > Validating if any messages should be announced')
        for msg in self.messages:
            if len(msg['Alert Triggers']) > 0:
                msg['Alert Triggers'].sort()
                if(msg['Alert Triggers'][0]) <= datetime.datetime.now():
                    message_header = (f'You have received a message from ' +
                                      f'{msg['sender_first_name']} {msg['sender_last_name']}: ')
                    voice = judyVoice(self.settings, self.bubble_creds)
                    voice.read_text(message_header + msg['Message'])
                    msg['Alert Triggers'].pop(0)

    def check_msg_fields(self, msg):
        '''
        Got through all the fields in the message to ensure that they are present and formatted correctly.
        :param msg:
        :return:
        '''

        msg['sender_first_name'] = self.check_key(msg, 'sender_first_name')
        msg['sender_last_name'] = self.check_key(msg, 'sender_last_name')
        msg['message'] = self.check_key(msg, 'message')

        msg['Modified Date'] = datetime.datetime.strptime(msg['Modified Date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        msg['Created Date'] = datetime.datetime.strptime(msg['Created Date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        msg['Expiration Date'] = msg['Modified Date'] + datetime.timedelta(hours=msg['Expiration'])

    def check_key(self, msg, key):
        '''
        Simple method to make sure that there is a key present in a specific dict
        :param msg:
        :param key:
        :return:
        '''
        if key in msg.keys():
            return msg[key]
        else:
            return ''


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

    # Need to set settings
    settings = {
        'photo_delay': '4',
        'accent': 'American',
        'trigger': 'Judy'
    }

    test_instance = messageHandler(credentials, settings)
    test_instance.get_messages()
    test_instance.clean_messages()
    for msg in test_instance.messages:
        print(msg)
    test_instance.alert_messages()