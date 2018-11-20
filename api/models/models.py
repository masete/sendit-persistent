


parcels = []


class Parcel:

    def __init__(self, parcel_id, parcel_location, parcel_destination, parcel_weight, parcel_description, status):
        self.parcel_id = parcel_id
        self.parcel_location = parcel_location
        self.parcel_destination = parcel_destination
        self.parcel_weight = parcel_weight
        self.parcel_description = parcel_description
        self.status = status

    def to_dict(self):
        """A method to Convert the parcel instance to a dictionary"""
        parcel = {
            'parcel_id': self.parcel_id,
            'parcel_location': self.parcel_location,
            'parcel_destination': self.parcel_destination,
            'parcel_weight': self.parcel_weight,
            'parcel_description': self.parcel_description,
            'status': self.status
        }
        return parcel


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

    @classmethod
    def is_admin(cls, user_id):
        from api.models.senditdb import DatabaseConnection
        db = DatabaseConnection()
        user = db.check_admin_status(user_id)
        if user:
            print(user.to_dict())
            if user.admin:
                return True
            return False
        return False





