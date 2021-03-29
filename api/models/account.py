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

    def get_full_name(self):
        return self.full_name

    def get_role(self):
        return self.role
    
    def to_json(self):
        return self.__dict__