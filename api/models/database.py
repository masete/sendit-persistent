import psycopg2
import os
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash


class DatabaseConnection:
    def __init__(self):
        self.commands = (
            """
            CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    role BOOLEAN DEFAULT FALSE NOT NULL
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
        try:
            # self.attributes = dict(dbname='senditdb',
            #                        user='postgres',
            #                        password='qwerty',
            #                        host='localhost',
            #                        port='5432')
            # self.connection = psycopg2.connect(**self.attributes, cursor_factory=RealDictCursor)
            if os.getenv("FLASK_ENV") == "production":
                self.connection = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)

            elif os.getenv("FLASK_ENV") == "TESTING":
                print('Connecting to test db')
                self.connection = psycopg2.connect(dbname='test_senditdb',
                                                   user='postgres',
                                                   password='qwerty',
                                                   host='localhost',
                                                   port='5432', cursor_factory=RealDictCursor)
            else:
                print('Connecting development db')
                self.connection = psycopg2.connect(dbname='senditdb',
                                                   user='postgres',
                                                   password='qwerty',
                                                   host='localhost',
                                                   port='5432', cursor_factory=RealDictCursor)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            for command in self.commands:
                self.cursor.execute(command)
        except Exception as error:
            print(f"error: {error}")

        self.cursor.execute("SELECT * FROM users WHERE email= '{}'".format("admin@gmail.com"))
        if self.cursor.fetchone():
            return None
        # set admin user
        hash_pwd = generate_password_hash("masete24")
        sql = "INSERT INTO users(username, email, password, role) VALUES('admin', 'admin@gmail.com', '{}', True)"\
            .format(hash_pwd)

        self.cursor.execute(sql)
        self.connection.commit()

    def drop_tables(self):
        query = "DROP TABLE IF EXISTS {} CASCADE"
        tabl_names = ["parcel, users"]
        for name in tabl_names:
            self.cursor.execute(query.format(name))

    def create_tables(self):
        for command in self.commands:
            self.cursor.execute(command)

