import psycopg2
import os


class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(dbname='senditdb',
                                           user='postgres',
                                           password='qwerty',
                                           host='localhost',
                                           port='5432')
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        print(self.cursor)


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






