class Entry():
    def __init__(self, timestamp, building, building_id, count, endpoint, endpoint_id, room_capacity):
        '''
        Used to initialize the creation of an entry
        '''

        self.timestamp = timestamp
        self.building = building
        self.building_id = building_id
        self.count = count
        self.endpoint = endpoint
        self.endpoint_id = endpoint_id
        self.room_capacity = room_capacity

    def get_building(self):
        '''
        Gets the building

        @returns a building name
        '''

        return self.building
    
    def get_building_id(self):
        '''
        Gets the building id

        @returns a building id
        '''

        return self.building_id

    def get_count(self):
        '''
        Gets the count for the room

        @returns a count
        '''

        return self.count
    
    def get_endpoint(self):
        '''
        Gets the endpoint name

        @returns endpoint name
        '''

        return self.endpoint
    
    def get_endpoint_id(self):
        '''
        Gets the endpoint id

        @returns the endpoint id
        '''

        return self.endpoint_id
    
    def get_room_capacity(self):
        '''
        Gets the room capacity

        @returns the room capacity
        '''

        return self.room_capacity
    
    def get_timestamp(self):
        '''
        Gets the timestamp of the room

        @returns the timestamp
        '''

        return self.timestamp

    def to_json(self):
        '''
        Gets the JSON representation of the model

        @returns a JSON object
        '''

        return self.__dict__