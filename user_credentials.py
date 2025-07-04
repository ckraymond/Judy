def get_user_credentials(name):
    email_map = {
        'Donald Trump': 'djt@judypatient.com',
        'Abraham Lincoln': 'al@judypatient.com',
        'Franklin Roosevelt': 'fdr@judypatient.com',
        'Ronald Regan': 'rwr@judypatient.com',
        'Colin Raymond': 'colin@judydevice.com'
    }

    pass_map = {
        'Donald Trump': 'b1{XF}7z',
        'Abraham Lincoln': ']K:kAh24',
        'Franklin Roosevelt': 'qTsF_7?9',
        'Ronald Regan': 'L]/4Cdo6',
        'Colin Raymond': '4Nk!>pG7'
    }

    if name not in email_map.keys():
        raise ValueError(f'{name} is not found in the list of user names.')

    return email_map[name], pass_map[name]

# Test to make sure it works
if __name__ == '__main__':
    email, password = get_user_credentials('Colin Raymond')
    print(email)
    print(password)