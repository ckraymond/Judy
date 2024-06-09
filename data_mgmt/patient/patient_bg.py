import logging

class patientBG():
    def __init__(self, response):
        self.mapping = {
            'schools': 'BG_Schools',
            'sports': 'BG_Sports',
            'foods': 'BG_Foods',
            'places': 'BG_Places',
            'hobbies': 'BG_Hobbies'
        }
        self.data = {}

        for item in self.mapping:
            try:
                self.data[item] = response[self.mapping[item]]
            except:
                logging.info('Background info ',self.mapping[item], ' does not exist.' )

    def __str__(self):
        return_str = '\n\nPatient Background\n------------------------------------------------------'
        for item in self.data:
            return_str += f'\n{item}: {self.data[item]}'
        return return_str