class Entry():
    def __init__(self, timestamp, building, building_id, count, endpoint, endpoint_id, room_capacity):
        self.timestamp = timestamp
        self.building = building
        self.building_id = building_id
        self.count = count
        self.endpoint = endpoint
        self.endpoint_id = endpoint_id
        self.room_capacity = room_capacity

    def get_building(self):
        return self.building
    
    def get_building_id(self):
        return self.building_id

    def get_count(self):
        return self.count
    
    def get_endpoint(self):
        return self.endpoint
    
    def get_endpoint_id(self):
        return self.endpoint_id
    
    def get_room_capacity(self):
        return self.room_capacity
    
    def get_timestamp(self):
        return self.timestamp

    def to_json(self):
        return self.__dict__