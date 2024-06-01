import openai           # Needed to support the call for OpenAI API
import logging           # always good to log info

def openai_api_call(query):
    '''
    Calls the OpenAI API using the system prompt and returns the answer
    :param query:
    :return: completion content
    '''

    # TODO: Need to adjust this so it is reading from a data file
    qry_params = {
        'model': 'gpt-3.5-turbo',
        'temp': 0.2,
        'sys_content': 'You are a personal assistant for someone who has a neurological condition.The person you are talking to often forgets what was last said so you should subtely remind them of what you talked about previously.You should be deferrential and respectful without being overly formal.'
    }

    logging.info('Contacting OpenAI with query: ', query)

    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model=qry_params['model'],
        temperature=qry_params['temp'],
        messages=[
            {"role": "system", "content": qry_params['sys_content']},
            {"role": "user", "content": query}
        ]
    )

    return completion.choices[0].message.content

def openai_api_keywords(query):
    keyword_gen_api_call = {
        'model': 'gpt-3.5-turbo',
        'temp': 0.0,
        'sys_content': 'You are reviewing data that may be used to power a GPT model in the future.' +
                       'Review user prompt and return no more than ten keywords that best represent ' +
                       'the intent of the message and would be useful for someone who was reviewing what ' +
                       'the message was in the future. They keywords should be returned in a comma delimited format.',
        'query': query
    }