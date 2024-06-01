# This script is used to generate a pickle formatted file which can be used to pull a preformatted script

import pickle
import openai

#Use this dict to create the structure you want
keyword_gen_api_call = {
    'model': 'gpt-3.5-turbo',
    'temp': 0.0,
    'sys_content': 'You are reviewing data that may be used to power a GPT model in the future.' +
                    'Review user prompt and return no more than ten keywords that best represent ' +
                    'the intent of the message and would be useful for someone who was reviewing what ' +
                    'the message was in the future. They keywords should be returned in a comma delimited format.',
    'query': 'I am missing my old friend Pedro. He was so fun and we often used to go fishing all the time. It was back when I was younger and my damn memory wasnt so bad.'
}

client = openai.OpenAI()

completion = client.chat.completions.create(
    model=keyword_gen_api_call['model'],
    temperature=keyword_gen_api_call['temp'],
    messages=[
        {"role": "system", "content": keyword_gen_api_call['sys_content']},
        {"role": "user", "content": keyword_gen_api_call['query']}
    ]
)

print(completion.choices[0].message.content)



