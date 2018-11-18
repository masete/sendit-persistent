import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.models import Parcel, Users, parcels, users_list
from passlib.hash import pbkdf2_sha256 as sha256


class DatabaseConnection:
    def __init__(self):
        self.commands = (
            """
            CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(200) NOT NULL
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

        self.connection = psycopg2.connect(dbname='senditdb',
                                           user='postgres',
                                           password='qwerty',
                                           host='localhost',
                                           port='5432')
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        print(self.cursor)
        for command in self.commands:
            self.cursor.execute(command)

    def get_user(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email='{}'".format(email))
        if self.cursor.fetchone():
            return True
        return False

    def get_user_by_username(self, username):
        by_username = "SELECT * FROM users WHERE username= '{}'".format(username)
        self.cursor.execute(by_username)
        return self.cursor.fetchone()

    def signup(self, username, email, password):
        if not self.get_user(email):

            hash_pwd = generate_password_hash(password)
            insert_user = "INSERT INTO users(username, email, password) VALUES('{}','{}','{}')".format(username, email, hash_pwd)
            self.cursor.execute(insert_user)
            return "user added"
        return "user exist"

    def login(self, email):
        if not self.get_user(email):
            return
        return "signup please"

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

    def insert_new_parcel(self, parcel_location, parcel_destination, parcel_weight, parcel_description, status):

        insert_parcel = "INSERT INTO parcel(parcel_location, parcel_destination, parcel_weight, parcel_description, " \
                        "status ) VALUES('{}','{}','{}','{}','{}')".format(parcel_location, parcel_destination,
                                                                           parcel_weight, parcel_description, status)
        self.cursor.execute(insert_parcel)
        return "parcel successfully created"

    def get_all_parcels(self):
        get_all_parcel = "SELECT * FROM parcel"
        self.cursor.execute(get_all_parcel)
        results = self.cursor.fetchall()
        if not results:
            return False
        for result in results:
            parcel = Parcel(result[0], result[1], result[2], result[3], result[4]).to_dict()
            parcels.append(parcel)
        return parcels

    def get_one_parcel(self, parcel_id):
        get_single_parcel = "SELECT * FROM parcel WHERE parcel_id = {}".format(parcel_id)
        self.cursor.execute(get_single_parcel)
        result = self.cursor.fetchone()
        if not result:
            return False
        parcel = Parcel(result[0], result[1], result[2], result[3], result[4]).to_dict()
        parcels.append(parcel)
        return parcel

    def find_parcel_by_user_id(self, user_id):
        parcel_by_user_id = "SELECT * FROM sales WHERE user_id = {}".format(user_id)
        self.cursor.execute(parcel_by_user_id)
        result = self.cursor.fetchall()
        if result:
            par = Parcel(result[0], result[1], result[2], result[3])
            return par

