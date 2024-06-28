import openai           # Needed to support the call for OpenAI API
import json

from api.promptcreate import promptCreate
from judylog.judylog import judylog

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
        judylog.info('openAIGPT.user_query > Initializing new query.')

        self.prompt = promptCreate(raw_query, user, history)

    def run_query(self):
        '''
        With information already loaded into the messages list we can now run the query to ChatGPT
        :return:
        '''

        judylog.info(f'openAIGPT.run_Query > Contacting OpenAI with query: {self.prompt.raw_query}')
        for msg in self.prompt.messages:
            judylog.debug(f'openAIGPT.run_query > {json.dumps(msg)}')

        client = openai.OpenAI()

        completion = client.chat.completions.create(
            model=self.model,
            temperature=self.temp,
            messages=self.prompt.messages
        )

        judylog.info(f'openAIGPT.run_Query > {completion}')

        print(f'openAIGPT.run_query > {type(completion.choices[0].message.content)}')
        return completion.choices[0].message.content

    def gen_summary(self, query, response):
        '''
            Gives a summary of a chatExchange, which is one part of a conversation
            :param query:
            :return:
            '''

        client = openai.OpenAI()

        completion = client.chat.completions.create(
            model=self.model,
            temperature=self.temp,
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

    def get_conv_summary(self, exch_list):
        '''
        Gives a summary of a conversation.
        :param exch_list:
        :return:
        '''
        messages = []

        messages.append({"role": "system",
                         "content": "Any response should be in a JSON format with three fields: summary, sentiment, and keywords."})
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
            model=self.model,
            temperature=self.temp,
            messages=messages
        )

        return json.loads(completion.choices[0].message.content)
