from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, password):
        self.id = email
        self.email = email
        self.password = password