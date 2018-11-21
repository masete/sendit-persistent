from werkzeug.security import generate_password_hash, check_password_hash
from api.models.database import DatabaseConnection

cursor = DatabaseConnection().cursor
users_list = []


class Users:

    def __init__(self, username=None, email=None, password=None, admin=False):
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin


    @staticmethod
    def get_user_by_username(username):
        result = "SELECT * FROM users WHERE username = '{}'".format(username)
        cursor.execute(result)
        query1 = cursor.fetchone()
        if not query1:
            return False
        return query1

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def fetch_user(self, user_id, username, password=None):

        fetch_user_query = f""" SELECT username, password FROM users
               WHERE username='{username}'
        """
        response = None
        # 1 query db
        cursor.execute(fetch_user_query)
        # 2 fetch result
        fetched_user = cursor.fetchone()
        if fetched_user:
            response = fetched_user
        else:
            response = {"error": "user does not exist"}
        return response

    def signup_user(self, username, email, password):

        password = generate_password_hash(password)
        user_exists_query = f"""
                 SELECT username from users WHERE username='{username}'
             """

        cursor.execute(user_exists_query)
        returned_user = cursor.fetchone()
        if returned_user:
            return False

        reqister_user_query = f""" INSERT INTO users (username, email, password) 
             VALUES('{username}', '{email}', '{password}')
                  """
        cursor.execute(reqister_user_query)

        user_exists_query1 = f"""
                         SELECT username from users WHERE username='{username}'
                     """
        cursor.execute(user_exists_query1)
        user1 = cursor.fetchone()
        return user1

    def check_admin_status(self, user_id):
        query = "SELECT * FROM users WHERE user_id = '{}'".format(user_id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            user = Users(result[0], result[1], result[2], result[3])
            return user
        return None

    def get_all_users(self):
        users_list.clear()
        get_all_users = "SELECT * FROM users"
        cursor.execute(get_all_users)
        results = cursor.fetchall()
        users_list.append(results)
        return users_list


