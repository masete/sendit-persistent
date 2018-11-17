import psycopg2
from werkzeug.security import generate_password_hash,check_password_hash


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
                    parcel_description VARCHAR(20) NOT NULL
                                                   
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

    def signup(self, username, email, password):
        if not self.get_user(email):
            insert_user = "INSERT INTO users(username,email,password) VALUES('{}','{}','{}')".format(username, email,
                                                                                                     password)
            self.cursor.execute(insert_user)
            return "user added"
        return "user exist"

    def login(self, email):
        if not self.get_user(email):
            return
        return "signup please"
