import openai           # Needed to support the call for OpenAI API
import logging           # always good to log info
import json

from init.judyparams import OPENAI_QUERY
from api.promptcreate import promptCreate

class openAIGPT:
    '''
    Wrapper class for all Open AI API calls to ChatGPT
    '''

    def __init__(self, model = 'gpt-3.5-turbo', temp = 0):
        self.model = model
        self.temp = temp

    def __str__(self):
        return f'{self.model} | {self.temp} | {','.join(self.message)[:100]}'

    def user_query(self, raw_query, user, history):
        '''
        Given a user query and their information, this submits a specific query to ChatGPT and returns the results.
        :param query:
        :param user:
        :return:
        '''
        #TODO: Give ability to short answer to specific number of words.
        logging.info('openAIGPT.user_query > Initializing new query.')

        self.prompt = promptCreate(raw_query, user, history)

    def run_query(self):
        '''
        With information already loaded into the messages list we can now run the query to ChatGPT
        :return:
        '''

        logging.info('Contacting OpenAI with query: ', self.prompt.raw_query)

        client = openai.OpenAI()

        completion = client.chat.completions.create(
            model=self.model,
            temperature=self.temp,
            messages=self.prompt.messages
        )

        logging.info('openAIGPT.run_Query > ', completion)
        print('openAIGPT.run_Query > ', completion)

        return completion.choices[0].message.content

class openAIWhisper:

    def __init__(self):
        logging.info('openAIWhisper.__ini__ > Initializing Whisper connection.')



def openai_api_call(query, history):
    '''
    Calls the OpenAI API using the system prompt and returns the answer
    :param query:
    :return: completion content
    '''

    # TODO: Need to adjust this so it is reading from a data file
    logging.info('Contacting OpenAI with query: ', query)

    # Pull all of the user info to be added into the query
    user_info = promptCreate()
    user_info.gen_prompt()

    # Get the last five questions and answers
    last_five = history[-5:]
    messages = build_messages(last_five, query, user_info.user_prompt)

    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model=OPENAI_QUERY['model'],
        temperature=OPENAI_QUERY['temp'],
        messages=messages
    )

    return completion.choices[0].message.content

def build_messages(last_five, query, user_prompt):
    messages = []

    messages.append({"role": "system", "content": OPENAI_QUERY['sys_content']})
    messages.append({"role": "user", "content": user_prompt})
    for item in last_five:
        messages.append({"role": "user", "content": item.query})
        messages.append({"role": "assistant", "content": item.response})
    messages.append({"role": "user", "content": query})

    return messages

def openai_api_summary(query, response):
    '''
    Ingests an exchange and produces a summary of the exchange.
    :param query:
    :return:
    '''

    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model=OPENAI_QUERY['model'],
        temperature=OPENAI_QUERY['temp'],
        messages=[
            {"role": "user", "content": query},
            {"role": "assistant", "content": response},
            {"role": "user", "content": """Provide your output in a JSON format with two keys: summary and keywords. 
            
            The summary field should have a summary of our above conversation one sentence. Be sure to call out both 
            what you think my mood is as well as identifying any people or places that I have asked about. Refer 
            to me in the summary as the patient and yourself as the assistant.
            
            The keywords field should be a comma-delimited list of any places, people, or events that are referenced
            in our conversation."""}
        ]
    )

    return json.loads(completion.choices[0].message.content)

def openai_conv_info(exch_list):
    messages = []

    messages.append({"role": "system", "content": "Any response should be in a JSON format with three fields: summary, sentiment, and keywords."})
    for exch in exch_list:
        messages.append({"role": "user", "content": exch.query})
        messages.append({"role": "system", "content": exch.response})
    messages.append({"role": "user", "content": """Provide your output in a JSON format with two keys: summary, sentiment, and keywords.

                Using the conversation above as a model the fields should have the following information:
                
                In summary, it should be a one sentence summary of the conversation that highlights what was talked about 
                and talking about any emotions or concerns that I have should be identified. Also, you should refer to me 
                as the patient and yourself as the assistant.
                
                In sentiment, assign a number between 1 and 5 for how I seem to be feeling. 1 would be extremely depressed 
                and 5 would be extremely happy.
                
                In keywords, provide a comma-delimited list of any places, people, or events that are referenced
                in our conversation. There should be at least one keyword and no more than 10."""})

    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model=OPENAI_QUERY['model'],
        temperature=OPENAI_QUERY['temp'],
        messages=messages
    )

    print(completion.choices[0].message.content)
    return json.loads(completion.choices[0].message.content)