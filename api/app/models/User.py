import uuid
class User(object):
    def __init__(self, id, user_name, first_name, last_name, password, account_type='standard_user'):
        self.id = id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.account_type = account_type