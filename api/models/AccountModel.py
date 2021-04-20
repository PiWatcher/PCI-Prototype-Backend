import bcrypt

class Account():
    def __init__(self, email, password, full_name, role="public"):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.role = role

    def check_password_hash(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def hash_password(self):
        self.password = bcrypt.hashpw(
            self.password.encode('utf-8'),
            bcrypt.gensalt()
        )

        # return instance
        return self

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email
        return self

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_full_name(self):
        return self.full_name

    def set_full_name(self, full_name):
        self.full_name = full_name
        return self

    def get_role(self):
        return self.role

    def set_role(self, role):
        self.role = role
        return self
    
    def to_json(self):
        return self.__dict__