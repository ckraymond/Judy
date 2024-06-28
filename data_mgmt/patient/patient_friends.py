from judylog.judylog import judylog
class patientFriends:

    def __init__(self, friends_list):
        self.mapping = {
            'bday': 'birthday',
            'deceased': 'deceased',
            'fname': 'first_name',
            'interests': 'interests',
            'lname': 'last_name',
            'location': 'location',
            'nname': 'nickname',
            'patient': 'Patient',
            'relationship': 'relationship'
        }
        self.data = []

        for friend in friends_list:
            new_friend = {}
            for item in self.mapping:
                try:
                    new_friend[item] = friend[self.mapping[item]]
                except:
                    judylog.info(f'patientFriends.__init__ > Friend info {self.mapping[item]} does not exist.')
            self.data.append(new_friend)
        judylog.debug(f'patientFriends.__init__ > {self.data}')

    def __str__(self):
        return_str = f'\n\nPatient Friends\n------------------------------------------------------'
        for friend in self.data:
            friend_str = '\n'
            for item in friend:
                friend_str += f'{item}: {friend[item]} '
            return_str += friend_str
        return return_str