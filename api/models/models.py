from api.models.database import DatabaseConnection
from flask import jsonify

cursor = DatabaseConnection().cursor

parcels = []


class Parcel:

    def __init__(self, parcel_id=None, parcel_location=None, parcel_destination=None, parcel_weight=None, parcel_description=None, status=None):
        self.parcel_id = parcel_id
        self.parcel_location = parcel_location
        self.parcel_destination = parcel_destination
        self.parcel_weight = parcel_weight
        self.parcel_description = parcel_description
        self.status = status
        self.cursor = cursor

    def insert_new_parcel(self, user_id, parcel_location, parcel_destination, parcel_weight, parcel_description,
                          status):
        insert_parcel = "INSERT INTO parcel(parcel_location, parcel_destination, parcel_weight, parcel_description, " \
                        "status ) VALUES('{}','{}','{}','{}','{}','{}')".format(user_id, parcel_location,
                                                                                parcel_destination,
                                                                                parcel_weight, parcel_description,
                                                                                status)
        self.cursor.execute(insert_parcel)
        return "parcel successfully created"

    def get_all_parcels(self):
        get_all_parcel = "SELECT * FROM parcel"
        self.cursor.execute(get_all_parcel)
        results = self.cursor.fetchall()
        return results

    def get_one_parcel(self, parcel_id):
        get_single_parcel = "SELECT * FROM parcel WHERE parcel_id = {}".format(parcel_id)
        self.cursor.execute(get_single_parcel)
        result = self.cursor.fetchone()
        return result

    def find_parcel_by_user_id(self, user_id):
        self.cursor.execute = "SELECT * FROM parcel WHERE user_id = {}".format(user_id)
        check_user_id = self.cursor.fetchall()
        print(user_id)
        parcels_by_user = []
        for parcel in check_user_id:
            parcels_by_user.append(parcel)
        return parcels_by_user

    def cancel_parcel(self, parcel_id):
        parcels = "SELECT * FROM parcel WHERE parcel_id = {}".format(parcel_id)
        self.cursor.execute(parcels)
        if not self.cursor.fetchone():
            return False
        cancel = "UPDATE parcel SET status = 'cancelled' WHERE parcel_id = {}".format(parcel_id)
        self.cursor.execute(cancel)
        parcels = "SELECT * FROM parcel WHERE parcel_id = {}".format(parcel_id)
        self.cursor.execute(parcels)
        parcel = self.cursor.fetchone()
        return parcel

    def change_destination(self, parcel_destination, parcel_id):
        change = "UPDATE parcel SET parcel_destination = '{}' WHERE parcel_id = '{}'".format(parcel_destination,
                                                                                             parcel_id)
        self.cursor.execute(change)

        query1 = "SELECT * FROM parcel WHERE parcel_id = {}".format(parcel_id)
        self.cursor.execute(query1)
        result1 = self.cursor.fetchone()

        return result1

    def admin_change_status(self, parcel_id, user_id, status):
        query = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if not data:
            return jsonify({"message": "there are no parcels currently intransit"})

        query1 = "  UPDATE parcel SET status = '{}' WHERE parcel_id = '{}'".format(status, parcel_id)
        self.cursor.execute(query1)

        query2 = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query2)
        return self.cursor.fetchone()

    def admin_change_location(self, parcel_id, user_id, parcel_location):
        query = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if not data:
            return jsonify({"message": "hey nothing to edit"})

        query1 = "  UPDATE parcel SET parcel_location = '{}' WHERE parcel_id = '{}'".format(parcel_location, parcel_id)
        self.cursor.execute(query1)

        query2 = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query2)
        return self.cursor.fetchone()



