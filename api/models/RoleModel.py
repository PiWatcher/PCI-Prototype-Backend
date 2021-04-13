class Role():
    def __init__(self, role_name, is_admin=False, can_view_raw=False):
        self.role_name = role_name
        self.is_admin = is_admin
        self.can_view_raw = can_view_raw

    def get_can_view_raw(self):
        return self.can_view_raw
    
    def get_is_admin(self):
        return self.is_admin

    def get_role_name(self):
        return self.get_role_name

    def to_json(self):
        return self.__dict__