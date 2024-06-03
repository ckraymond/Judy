import datetime

usernames = {
    'fname': 'Judith',
    'lname': 'Jultquist',
    'mname': 'Raymond',
    'nname': 'Judy'
}

biography = {
    'names': usernames,
    'bday': datetime.date(1950,4,15),
    'home': 'Missoula'
}

def create_person(fname, lname, nname, relationship, location, bday, interests, deceased):
    return {
        'fname': fname,
        'lname': lname,
        'relationship': relationship,
        'location': location,
        'bday': bday,
        'interests': interests,
        'deceased': deceased
    }

people = [
    create_person('Jacky', 'Norris', None, 'sister',
                  'Missoula', None, [], False),
    create_person('Bruce', 'Raymond', None, 'brother',
                      'Denver', None, [], False),
    create_person('Brian', 'Raymond', None, 'brother',
                      'Denver', None, [], True),
    create_person('Douglas', 'Raymond', 'Doug', 'brother',
                      'Seattle', None, [], False),
    create_person('Andrew', 'Norris', None, 'brother',
                      'Missoula', None, [], False),
    create_person('Colin', 'Raymond', None, 'brother',
                      'Missoula', datetime.date(1979,8,6), [], False),
    create_person('Barbara', None, 'Barb', 'friend',
                      'New York', None, [], False)
    ]

places = [
    {
        'name': 'Missoula',
        'reason': 'My home'
    },
    {
        'name': 'Ossining',
        'reason': 'Where I used to live'
    },
    {
        'name': 'The barn',
        'reason': 'I used to ride horses there for a long time'
    }
]


# dates = [
#     {
#         'date': datetime.date(2001,9,11),
#         'name': '9/11',
#         'reason': 'Its a national tragedy',
#         'description': ''
#     }
# ]

events = [
    {
        'date': datetime.date(2001, 6, 5),
        'name': 'Colins graduation',
        'description': 'When users brother Colin graduated from West Point. I was there and had a great time.'
    },
    {
        'date': datetime.date(2024, 12, 15),
        'name': 'I moved to Missoula',
        'description': 'This is when I moved from my home in Ossining to Missoula with Jackys help. It was a tough transition but I am happier now.'
    }
]

interests = [
    'horseback riding',
    'writing',
    'cats',
    'reading',
    'yankees baseball'
]

# asks = [
#     {
#         'ask': 'I want to make sure that my cats are okay.'
#     }
# ]

faqs = [
    {
        'question': 'Where are my cats?',
        'answer': 'They live with you in your apartment at the springs.'
    }
]

pets = [
    {
        'name': 'Ginger',
        'type': 'cat',
        'phys_desc': 'organe and stripey'
    }
]

test_user_info = {
     'userid': 1,
     'biography': biography,

     # The important people in her life
     'people': people,

     # Important places in her life
     'places': places,

     # Important events in her life
     'events': events,

     # Important dates she should remember outside of her birthday or others' birthdays
     # 'dates': dates,

     # Things the user has asked the system or talked about
     # 'asks': asks,

     # What are the users interests
     'interests': interests,

    # What are the commonly asked questions the user has
    'faqs': faqs
 }

# print(test_user_info)