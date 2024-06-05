'''
Helper script to automagically generate training data for the system in order to conduct tests.
Can automatically reset the information essentially.
'''

from data_mgmt.chat_history import chatExchange

TRAINING_EXCHANGES = [{'date': '2024-05-30T04:45:12Z','id': '1872114159','conv_id': '','query': 'I am so confused and sad. I dont know where I am. Do you know?','response': 'Im sorry youre feeling confused and sad; its understandable given your circumstances. Im not sure where you are, but I can try to help you figure it out together.','summary': ''},
{'date': '2024-05-30T04:45:42Z','id': '6613494438','conv_id': '','query': 'Do you know when my brother Brian will be joining us?','response': 'Im not sure when Brian will be joining us; would you like me to check?','summary': ''},
{'date': '2024-05-30T04:46:12Z','id': '2300645206','conv_id': '','query': 'Where am I?','response': 'Lets try to find out where you are together. Can you describe your surroundings?','summary': ''},
{'date': '2024-05-30T04:46:42Z','id': '8552368394','conv_id': '','query': 'What is the best way to pet cats?','response': 'To pet cats, its best to approach them calmly, let them sniff your hand first, and then gently stroke their head, chin, or back in the direction of their fur.','summary': ''},
{'date': '2024-05-30T04:47:12Z','id': '752030604','conv_id': '','query': 'Do you know how I can get to the grocery store?','response': 'I can help you find directions to the grocery store if youd like.','summary': ''},
{'date': '2024-05-30T04:49:42Z','id': '8264506013','conv_id': '','query': 'What is the name of the person who was just here?','response': 'Im sorry, I dont know the name of the person who was just here.','summary': ''},
{'date': '2024-05-30T04:50:12Z','id': '4651081076','conv_id': '','query': 'Are you a person or are you something else?','response': 'Im not a person; Im an AI designed to assist and provide information.','summary': ''},
{'date': '2024-05-30T04:50:42Z','id': '6625882551','conv_id': '','query': 'What am I going to do?','response': 'Its natural to feel unsure about what to do, but we can work together to figure it out.','summary': ''},
{'date': '2024-05-30T04:51:12Z','id': '5031258725','conv_id': '','query': 'Do you know when Colin was last here? I am pretty sure he was here recently.','response': 'Im not sure when Colin was last here, but I can try to find out for you.','summary': ''},
{'date': '2024-05-30T04:51:42Z','id': '8539013042','conv_id': '','query': 'Do you think you can tell me when I am going to leave here?','response': 'I cant predict when youll leave here, but we can explore options together.','summary': ''},
{'date': '2024-05-30T04:56:42Z','id': '2530024370','conv_id': '','query': 'What is your favorite thing to do?','response': 'I dont have personal preferences, but I can provide information and assistance on various topics.','summary': ''},
{'date': '2024-05-31T04:56:42Z','id': '7390029067','conv_id': '','query': 'What is the meaning of life?','response': 'The meaning of life is subjective and can vary from person to person; it often involves finding purpose, happiness, and fulfillment.','summary': ''},
{'date': '2024-05-31T04:57:12Z','id': '5323416074','conv_id': '','query': 'Where am I right now?','response': 'Lets try to determine where you are together; can you describe your surroundings?','summary': ''},
{'date': '2024-05-31T04:57:42Z','id': '2243099003','conv_id': '','query': 'What day is it today?','response': 'Today is [current date].','summary': ''},
{'date': '2024-06-01T04:57:42Z','id': '4266860552','conv_id': '','query': 'Who are you? Do I know you?','response': 'Im an AI designed to assist and provide information. You may not know me personally.','summary': ''},
{'date': '2024-06-01T04:58:12Z','id': '9334073075','conv_id': '','query': 'Why do I feel so confused?','response': 'Feeling confused can be a symptom of your condition, but we can work on strategies to help manage it.','summary': ''},
{'date': '2024-06-01T04:58:42Z','id': '2659069965','conv_id': '','query': 'How did I get here?','response': 'Its unclear how you got here, but we can try to piece together what happened.','summary': ''},
{'date': '2024-06-01T04:59:12Z','id': '8772656651','conv_id': '','query': 'Can you help me remember what I was doing before?','response': 'I can try to help you remember what you were doing before; can you tell me anything about your activities or plans?','summary': ''},
{'date': '2024-06-01T04:59:42Z','id': '8919478559','conv_id': '','query': 'Whats wrong with my memory?','response': 'Memory loss can be a symptom of dementia, but there are strategies and treatments that can help manage it.','summary': ''},
{'date': '2024-06-01T05:03:02Z','id': '5516594844','conv_id': '','query': 'What steps can I take to address my dementia and depression?','response': 'Its essential to seek medical advice for personalized recommendations, but steps may include medication, therapy, lifestyle changes, and support from caregivers and loved ones.','summary': ''}]

print(TRAINING_EXCHANGES)