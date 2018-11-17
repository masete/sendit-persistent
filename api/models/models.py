class Parcel:

    def __init__(self, parcel_id, parcel_location, parcel_destination, parcel_weight, parcel_description, user_id,status):
        self.parcel_id = parcel_id
        self.parcel_location = parcel_location
        self.parcel_destination = parcel_destination
        self.parcel_weight = parcel_weight
        self.parcel_description = parcel_description
        self.user_id = user_id
        self.status = status

    def to_dict(self):
        """A method to Convert the parcel instance to a dictionary"""
        parcel = {
            'parcel_id': self.parcel_id,
            'parcel_location': self.parcel_location,
            'parcel_destination': self.parcel_destination,
            'parcel_weight': self.parcel_weight,
            'parcel_description': self.parcel_description,
            'user_id': self.user_id,
            'status': self.status
        }
        return parcel




class Users:

    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self):
        user = {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
        return user
