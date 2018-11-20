import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.models import Parcel, Users, parcels, users_list
from flask import jsonify


class DatabaseConnection:
    def __init__(self):
        self.commands = (
            """
            CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    an_admin BOOLEAN DEFAULT FALSE NOT NULL
                    )
            
            """,
            """
                 CREATE TABLE IF NOT EXISTS parcel (                    
                    parcel_id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(user_id),
                    parcel_location VARCHAR(20) NOT NULL,
                    parcel_destination VARCHAR(20) NOT NULL,
                    parcel_weight INTEGER NOT NULL, 
                    parcel_description VARCHAR(20) NOT NULL,
                    status VARCHAR(20) NOT NULL
                                                   
                )
            """
        )
        #from run import app
        if os.getenv("FLASK_ENV") == "production":
            self.connection = psycopg2.connect(os.getenv("DATABASE.URL"))

        elif os.getenv("FLASK_ENV") == "TESTING":
            print('Connecting to test db')
            self.connection = psycopg2.connect(dbname='test_senditdb',
                                               user='postgres',
                                               password='qwerty',
                                               host='localhost',
                                               port='5432')
        else:
            print('Connecting development db')
            self.connection = psycopg2.connect(dbname='senditdb',
                                               user='postgres',
                                               password='qwerty',
                                               host='localhost',
                                               port='5432')
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        print(self.cursor)
        self.create_tables()
        self.create_admin()

    def drop_tables(self):
        query = "DROP TABLE IF EXISTS {} CASCADE"
        tabl_names = ["parcel, users"]
        for name in tabl_names:
            self.cursor.execute(query.format(name))

    def create_tables(self):
        for command in self.commands:
            self.cursor.execute(command)

    def create_admin(self):
        self.cursor.execute("SELECT * FROM users WHERE email= '{}'".format("admin@gmail.com"))
        if self.cursor.fetchone():
            return None
        # set admin user
        hash_pwd = generate_password_hash("masete24")
        self.cursor.execute("INSERT INTO users(username, email, password, an_admin) VALUES('admin', 'admin@gmail.com', "
                            "'{}', true)".format(hash_pwd))

    def get_user_by_id(self, user_id):
        get_user = self.cursor.execute("SELECT * FROM users WHERE user_id = '{}'".format(user_id))
        self.cursor.execute(get_user)
        result = self.cursor.fetchone()
        if result:
            user = Users(result[0], result[1], result[2], result[3]).to_dict()
            return user

    def check_admin_status(self, user_id):
        query = "SELECT * FROM users WHERE user_id = '{}'".format(user_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            user = Users(result[0], result[1], result[2], result[3], result[4])  # .to_dict()
            return user
        return None

    def get_user(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email='{}'".format(email))
        if self.cursor.fetchone():
            return True
        return False

    def login(self, username, password):
        query = "SELECT * FROM users WHERE username='{}'".format(username)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if not result:
            return False
        if check_password_hash(result[3], password):
            user = Users(result[0], result[1], result[2], result[3], result[4])  # .to_dict()
            return user
        return False

    def get_user_by_username(self, username):
        by_username = "SELECT * FROM users WHERE username= '{}'".format(username)
        self.cursor.execute(by_username)
        return self.cursor.fetchone()

    def signup(self, username, email, password):
        if not self.get_user(email):
            hash_pwd = generate_password_hash(password)
            insert_user = "INSERT INTO users(username, email, password) VALUES('{}','{}','{}')".format(username, email,
                                                                                                       hash_pwd)
            self.cursor.execute(insert_user)
            return "user added"
        return "user exist"

    def get_all_users(self):
        users_list.clear()
        get_all_users = "SELECT * FROM users"
        self.cursor.execute(get_all_users)
        results = self.cursor.fetchall()
        if not results:
            return False
        for result in results:
            user = Users(result[0], result[1], result[2], result[3]).to_dict()
            users_list.append(user)
        return users_list

    def insert_new_parcel(self, user_id, parcel_location, parcel_destination, parcel_weight, parcel_description,
                          status):

        insert_parcel = "INSERT INTO parcel(user_id, parcel_location, parcel_destination, parcel_weight, parcel_description, " \
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
        if not results:
            return False
        for result in results:
            parcel = Parcel(result[0], result[1], result[2], result[3], result[4], result[5]).to_dict()
            parcels.append(parcel)
        return parcels

    def get_one_parcel(self, parcel_id):
        get_single_parcel = "SELECT * FROM parcel WHERE parcel_id = {}".format(parcel_id)
        self.cursor.execute(get_single_parcel)
        result = self.cursor.fetchone()
        if not result:
            return False
        parcel = Parcel(result[0], result[1], result[2], result[3], result[4], result[5]).to_dict()
        parcels.append(parcel)
        return parcel

    def find_parcel_by_user_id(self, user_id):
        self.cursor.execute("SELECT * FROM parcel WHERE user_id = {}".format(user_id))
        check_user_id = self.cursor.fetchall()
        parcels_by_user = []
        for parcel in check_user_id:
            pcl = {
                "parcel_id": parcel[0],
                "user_id": parcel[1],
                "parcel_location": parcel[2],
                "parcel_destination": parcel[3],
                "parcel_weight": parcel[4],
                "parcel_description": parcel[5],
                "status": parcel[6]
            }
            parcels_by_user.append(pcl)
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
        pcl = {
            "parcel_id": parcel[0],
            "user_id": parcel[1],
            "parcel_location": parcel[2],
            "parcel_destination": parcel[3],
            "parcel_weight": parcel[4],
            "parcel_description": parcel[5],
            "status": parcel[6]
        }
        return [pcl]

    def change_destination(self, parcel_destination, parcel_id):
        # query = "SELECT * FROM parcel WHERE parcel_id = {} AND user_id = {}".format(parcel_id, user_id)
        # self.cursor.execute(query)
        # if not self.cursor.fetchone():
        # return False
        change = "UPDATE parcel SET parcel_destination = '{}' WHERE parcel_id = '{}'".format(parcel_destination,
                                                                                             parcel_id)
        self.cursor.execute(change)
        # result = self.cursor.fetchone()
        # # parcel_id, parcel_location, parcel_destination, parcel_weight, parcel_description, status)
        #
        # parcel = Parcel(result[0], result[1], result[2], result[3], result[4], result[5]).to_dict()
        return True

    def change(self, parcel_id, user_id, parcel_destination):
        query = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if not data:
            return jsonify({"message": "there is not data"})
        if data[1] != user_id:
            return jsonify({"message": "you cant change this destination"})

        query1 = "UPDATE parcel SET parcel_destination = '{}' WHERE parcel_id = '{}'".format(parcel_destination,
                                                                                             parcel_id)
        self.cursor.execute(query1)
        self.connection.commit()

        query2 = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query2)
        return self.cursor.fetchone()

    def admin_change_status(self, parcel_id, user_id, status):

        query = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if not data:
            return jsonify({"message": "there are no parcels currently intransit"})
        if data[1] != user_id:
            return jsonify({"message": "hey, you dont have rights to edit this"})

        query1 = "  UPDATE parcel SET status = '{}' WHERE parcel_id = '{}'".format(status, parcel_id)
        self.cursor.execute(query1)
        self.connection.commit()

        query2 = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query2)
        return self.cursor.fetchone()

    def admin_change_location(self, parcel_id, user_id, parcel_location):

        query = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if not data:
            return jsonify({"message": "hey nothing to edit"})
        if data[1] != user_id:
            return jsonify({"message": "hey, you dont have rights to edit this"})

        query1 = "  UPDATE parcel SET parcel_location = '{}' WHERE parcel_id = '{}'".format(status, parcel_id)
        self.cursor.execute(query1)
        self.connection.commit()

        query2 = "SELECT * FROM parcel WHERE parcel_id = '{}'".format(parcel_id)
        self.cursor.execute(query2)
        return self.cursor.fetchone()
