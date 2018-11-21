import psycopg2
import os
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash


class DatabaseConnection:
    def __init__(self):
        self.commands = (
            """
            CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    role VARCHAR(25)
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

        self.attributes = dict(dbname='senditdb',
                               user='postgres',
                               password='qwerty',
                               host='localhost',
                               port='5432')
        """

        if os.getenv("FLASK_ENV") == "production":
            self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))

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
        """

        try:
            self.connection = psycopg2.connect(**self.attributes, cursor_factory=RealDictCursor)
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
        sql = "INSERT INTO users(username, email, password, role) VALUES('admin', 'admin@gmail.com', '{}', 'admin')"\
            .format(hash_pwd)

        self.cursor.execute(sql)
        self.connection.commit()
