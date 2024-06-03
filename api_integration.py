import openai           # Needed to support the call for OpenAI API
import logging           # always good to log info

from judyparams import OPENAI_QUERY

def openai_api_call(query):
    '''
    Calls the OpenAI API using the system prompt and returns the answer
    :param query:
    :return: completion content
    '''

    # TODO: Need to adjust this so it is reading from a data file
    print(OPENAI_QUERY)

    logging.info('Contacting OpenAI with query: ', query)

    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model=OPENAI_QUERY['model'],
        temperature=OPENAI_QUERY['temp'],
        messages=[
            {"role": "system", "content": OPENAI_QUERY['sys_content']},
            {"role": "user", "content": query}
        ]
    )

    return completion.choices[0].message.content

def openai_api_keywords(query):
    '''
    Method to take a query and pull out several keywords. Intent is to use these keywords later in otder to
    have a sense of history.
    :param query:
    :return:
    '''
    keyword_gen_api_call = {
        'model': 'gpt-3.5-turbo',
        'temp': 0.0,
        'sys_content': 'You are reviewing data that may be used to power a GPT model in the future.' +
                       'Review user prompt and return no more than ten keywords that best represent ' +
                       'the intent of the message and would be useful for someone who was reviewing what ' +
                       'the message was in the future. They keywords should be returned in a comma delimited format.',
        'query': query
    }