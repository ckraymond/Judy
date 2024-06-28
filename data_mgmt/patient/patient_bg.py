from judylog.judylog import judylog

class patientBG:
    def __init__(self, interest):
        self.data = {
            'school': [],
            'sport': [],
            'food': [],
            'place': [],
            'hobby': [],
            'other': []
        }

        for item in interest:
            self.data[item['type']].append(item['interest'])

        judylog.debug(f'patientBG.__init__ > {self.data}')

    def __str__(self):
        return_str = '\n\nPatient Background\n------------------------------------------------------'
        for item in self.data:
            return_str += f'\n{item}: {self.data[item]}'
        return return_str