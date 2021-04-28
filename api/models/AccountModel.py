import bcrypt

class Account():
    def __init__(self, email, password, full_name, role="public"):
        '''
        Used to initialize the creation of an account
        '''

        self.email = email
        self.password = password
        self.full_name = full_name
        self.role = role

    def check_password_hash(self, password):
        '''
        Used to check if the given password matches with an accounts password has

        @param password to be checked against

        @return a boolean value
        '''

        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def hash_password(self):
        '''
        Hashes the password that is given

        @returns an instance of itself
        '''

        self.password = bcrypt.hashpw(
            self.password.encode('utf-8'),
            bcrypt.gensalt()
        )

        # return instance
        return self

    def get_email(self):
        '''
        Gets the email for an account
        
        @returns an email
        '''

        return self.email

    def set_email(self, email):
        '''
        Sets the email for an account

        @param email the email to set too

        @returns an instance of itself
        '''

        self.email = email
        return self

    def get_password(self):
        '''
        Gets the password from an account

        @returns the password
        '''

        return self.password

    def set_password(self, password):
        '''
        Sets the password for an account

        @param password the password to set too
        '''

        self.password = password

    def get_full_name(self):
        '''
        Gets the full name for an account

        @returns the full name
        '''

        return self.full_name

    def set_full_name(self, full_name):
        '''
        Sets the full name for an account

        @param full_name full name to set the account too

        @returns an instance of itself
        '''

        self.full_name = full_name
        return self

    def get_role(self):
        '''
        Gets the role for the account

        @returns the role
        '''

        return self.role

    def set_role(self, role):
        '''
        Sets the role for the account

        @param role role to be set

        @returns an instance of itself
        '''

        self.role = role
        return self
    
    def to_json(self):
        '''
        JSON representation of the account

        @returns a JSON object
        '''
        
        return self.__dict__