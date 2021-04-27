class Role():
    def __init__(self, role_name, is_admin=False, can_view_raw=False):
        '''
        Initializes a new role
        '''

        self.role_name = role_name
        self.is_admin = is_admin
        self.can_view_raw = can_view_raw

    def get_can_view_raw(self):
        '''
        Gets the can_view_raw property from the role

        @returns boolean value
        '''

        return self.can_view_raw
    
    def get_is_admin(self):
        '''
        Gets the admin property from the role

        @returns boolean value
        '''

        return self.is_admin

    def get_role_name(self):
        '''
        Gets the name of the role

        @returns the name of the role
        '''

        return self.get_role_name

    def to_json(self):
        '''
        Returns a JSON representation of the model

        @returns a JSON object
        '''

        return self.__dict__