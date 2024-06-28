def get_user_credentials(name):
    email_map = {
        'Donald Trump': 'djt@judypatient.com',
        'Abraham Lincoln': 'al@judypatient.com',
        'Franklin Roosevelt': 'fdr@judypatient.com',
        'Ronald Regan': 'rwr@judypatient.com'
    }

    pass_map = {
        'Donald Trump': 'b1{XF}7z',
        'Abraham Lincoln': ']K:kAh24',
        'Franklin Roosevelt': 'qTsF_7?9',
        'Ronald Regan': 'L]/4Cdo6'
    }

    return email_map[name], pass_map[name]

# Test to make sure it works
if __name__ == '__main__':
    email, password = get_user_credentials('Ronald Regan')
    print(email)
    print(password)