users_list = []


class Users:

    def __init__(self, user_id, username, email, password, admin=False):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin

    def to_dict(self):
        user = {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'admin': self.admin
        }
        return user