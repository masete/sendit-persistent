import unittest
import json
from api.models.database import DatabaseConnection


from run import create_app

"""
export FLASK_ENV=TESTING
echo $FLASK_ENV
"""


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()
        db = DatabaseConnection()
        db.create_tables()

    def tearDown(self):
        with self.app as app:
            db = DatabaseConnection()
            db.drop_tables()

    def test_logging_user_that_is_not_in_system(self):
        login = dict(username="admin", password="admin")
        request = self.app.post('/api/auth/login', json=login)
        response = json.loads(request.data.decode())
        self.assertIn('first signup', response['message'])

    def test_create_user(self):
        signup = dict(username="joel", email="joel@gmail.com", password="joel1234")
        request = self.app.post('/api/auth/signup', json=signup)
        response = json.loads(request.data.decode())
        self.assertIn('signedup user', str(response))
        self.assertEqual(request.status_code, 201)

    def test_log_in_user_in_system(self):
        signup = dict(username="joel", email="joel@gmail.com", password="joel1234")
        request = self.app.post('/api/auth/signup', json=signup)
        self.assertEqual(request.status_code, 201)
        request = self.app.post('/api/auth/login', json=signup)
        self.assertEqual(request.status_code, 200)
        response = json.loads(request.data.decode())
        self.assertIn('logged in successfully', response['message'])

    def get_admin_token(self):
        login = dict(username="admin", password="masete24")
        request = self.app.post('/api/auth/login', json=login)
        response = json.loads(request.data.decode())
        print('token response', str(response))
        token = response['access_token']
        return token

    def test_create_parcel(self):
        token = self.get_user_token()

        parcel_order = dict(parcel_description='some important stuff', parcel_location="mbarara", parcel_destination="kitgum",
                            parcel_weight=34, status="pending")

        request1 = self.app.post('/api/v1/parcel', json=parcel_order, headers={'Authorization': 'Bearer ' + token})
        response1 = json.loads(request1.data.decode())
        self.assertIn("parcel with description", response1["message"])

    def get_user_token(self):
        signup = dict(username="masete", email="masete@gmail.com", password="masete24")
        request = self.app.post('/api/auth/signup', json=signup)
        login = dict(username="masete", password="masete24")
        request = self.app.post('/api/auth/login', json=login)
        response = json.loads(request.data.decode())
        print('token response', str(response))
        token = response['access_token']
        return token

    def test_get_all_parcel(self):
        pass

    def test_get_single_parcel(self):
        token = self.get_user_token()

        post_add2 = dict(parcel_id=1, parcel_location="mbale", parcel_destination="manafwa", parcel_weight=23,
                         parcel_description="mangoes", status="pending")
        response1 = self.app.post('/api/v1/parcel', json=post_add2,
                                    headers={'Authorization': 'Bearer ' + token})
        response = self.app.get('/api/v1/parcel/1', headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 200)
        #assert json.loads(post_add2.data)['parcel_location'] == 'mbale'
        #assert response.status_code == 200
        #assert response.headers["Content-Type"] == "application/json"

        #
        # login = dict(username="admin",email="" password="admin")
        # request = self.app.post('/api/auth/login', json=login)
        # response = json.loads(request.data.decode())
        # self.assertIn('user added...', str(response))
        # #token = json.loads(response1.data)['access_token']
        # post_signup = dict(username="eugene", email="eugene@gmail.com", password="cohort")
        # response = self.app.post('/api/auth/signup', json=post_signup,
        #                          headers={'Authorization': 'Bearer ' + token})
        # assert json.loads(response.data)['message'] == "igaa4 has successfully been added to staff"
        # assert response.status_code == 201
        # assert response.headers["Content-Type"] == "application/json"
        #
        # login_result = self.app.post('/api/auth/login', content_type='application/json',
        #                             data=json.dumps(
        #                                            dict(
        #                                                username=self.login_field['username'],
        #                                                password=self.login_field['password'])
        #                                        )
        #
        #                                  )
        # self.result = json.loads(login_result.data)
        # self.user_generated_token = self.result['token']
    #
    # def test_token(self):
    #     self.assertNotEqual(self.result['token'], " ")
    #
    # def signup_user(self):
    #     register_user = dict(username="masete", email="masete@gmail.com", password=12345)
    #     response = self.app.post('/api/auth/signup', json=register_user, headers={"token": self.user_generated_token})
    #     assert "message" in str(response.data)
    #
    # def login_user(self):
    #     register_user = dict(username="masete", email="masete@gmail.com", password=12345)
    #     response = self.app.post('/api/auth/signup', json=register_user, headers={"token": self.user_generated_token})
    #     assert "message" in str(response.data)
    #
    # def test_data_structure(self):
    #     self.assertTrue(isinstance(parcel_orders, list))
    #
    # def test_create_parcel(self):
    #     post_order = dict(parcel_location="kisumu", parcel_destination="meru", parcel_weight=48,
    #                       parcel_description="apples", user_id=1, status="pending")
    #     response = self.app.post('/api/v1/parcel', json=post_order, headers={"token": self.user_generated_token})
    #     assert "message" in str(response.data)
    #     assert response.status_code == 201
    #     assert response.headers["Content-Type"] == "application/json"
    #
    # def test_empty_parcel_location_fields(self):
    #     post_order = dict(parcel_location=" ", parcel_destination="meru", parcel_weight=48,
    #                       parcel_description="apples",user_id=1,  status="pending")
    #     response = self.app.post('/api/v1/parcel', json=post_order,headers={"token": self.user_generated_token})
    #     assert "error" in str(response.data)
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "parcel location can not be parced empty string" in json.loads(response.data)['error']['parcel_location']
    #
    # def test_empty_parcel_destination_fields(self):
    #     post_order = dict(parcel_location="kisumu", parcel_destination=" ", parcel_weight=48,
    #                       parcel_description="apples",user_id=1, status="pending")
    #     response = self.app.post('/api/v1/parcel', json=post_order ,headers={"token": self.user_generated_token})
    #     assert "error" in str(response.data)
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "parcel destination can not be parced empty string" in json.loads(response.data)['error']['parcel_destination']
    #
    # def test_empty_parcel_weight_fields(self):
    #     post_order = dict(parcel_location="kisumu", parcel_destination="mbale", parcel_weight= -1,
    #                       parcel_description="apples", user_id=1, status="pending")
    #     response = self.app.post('/api/v1/parcel', json=post_order,headers={"token": self.user_generated_token})
    #     assert "error" in str(response.data)
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "weight cant be less than " in json.loads(response.data)['error']['parcel_weight']
    #
    # def test_empty_parcel_description_fields(self):
    #     post_order = dict(parcel_location="kisumu", parcel_destination="mbale", parcel_weight= 78,
    #                       parcel_description=" ",user_id=1, status="pending")
    #     response = self.app.post('/api/v1/parcel', json=post_order, headers={"token": self.user_generated_token})
    #     assert "error" in str(response.data)
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "parcel description can not be parced empty string" in json.loads(response.data)['error']['parcel_description']
    #
    # def test_empty_status_fields(self):
    #     post_order = dict(parcel_location="kisumu", parcel_destination="mbale", parcel_weight=78,
    #                       parcel_description="apples", user_id=1, status=" ")
    #     response = self.app.post('/api/v1/parcel', json=post_order, headers={"token": self.user_generated_token})
    #     assert "error" in str(response.data)
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "parcel status can not be parcel empty string" in json.loads(response.data)['error']['status']

    #def test_user_id_fields(self):
        #post_order = dict(parcel_location="kisumu", parcel_destination="mbale", parcel_weight=78,
                          #parcel_description="apples", user_id=-1, status="pending")
        #response = self.app.ppost('/api/v1/parcel', json=post_order, headers={"token": self.user_generated_token})
        #assert "error" in str(response.data)
        #assert response.status_code == 400
        #assert response.headers["Content-Type"] == "application/json"
        #assert "user_id cant be less than 0" in json.loads(response.data)['error']['user_id']

    #def test_invalid_parcel_location_field_inputs(self):
        #post_order = dict(parcel_location=674, parcel_destination="mbale", parcel_weight=78,
                          #parcel_description="apples", user_id=-1, status="pending")
        #response = self.app.post('/api/v1/parcel', json=post_order, headers={"token": self.user_generated_token})
        #assert response.status_code == 400
        #assert response.headers["Content-Type"] == "application/json"
        #assert "should be a string" == json.loads(response.data)['error']['parcel_location']

    #def test_invalid_parcel_destination_field_inputs(self):
        #post_order = dict(parcel_location="naalya", parcel_destination=89, parcel_weight=78,
                          #parcel_description="apples", user_id=1, status="pending")
        #response = self.app.post('/api/v1/parcel', json=post_order,headers={"token": self.user_generated_token} )
        #assert response.status_code == 400
        #assert response.headers["Content-Type"] == "application/json"
        #assert "should be a string" == json.loads(response.data)['error']['parcel_destination']

    # def test_invalid_status_field_inputs(self):
    #     post_order = dict(parcel_location="naalya", parcel_destination="egypt", parcel_weight=78,
    #                       parcel_description="apples", user_id=1, status=89)
    #     response = self.app.post('/api/v1/parcel', json=post_order,headers={"token": self.user_generated_token} )
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "status should be a string" == json.loads(response.data)['error']['status']
    #
    # def test_user_id_field_inputs(self):
    #     post_order = dict(parcel_location="naalya", parcel_destination="egypt", parcel_weight=78,
    #                       parcel_description="apples", user_id="nine", status=90)
    #     response = self.app.post('/api/v1/parcel', json=post_order,headers={"token": self.user_generated_token} )
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "user_id should be an integar" == json.loads(response.data)['error']['user_id']
    #
    # def test_invalid_parcel_weight_field_inputs(self):
    #     post_order = dict(parcel_location="naalya", parcel_destination="moroto", parcel_weight="five",
    #                       parcel_description="apples", user_id=1, status="pending")
    #     response = self.app.post('/api/v1/parcel', json=post_order, headers={"token": self.user_generated_token})
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "should be an integar" == json.loads(response.data)['error']['parcel_weight']
    #
    # def test_invalid_parcel_description_field_inputs(self):
    #     post_order = dict(parcel_location="naalya", parcel_destination="moroto", parcel_weight=6,
    #                       parcel_description=-40, user_id=1, status="pending")
    #     response = self.app.post('/api/v1/parcel', json=post_order, headers={"token": self.user_generated_token})
    #     assert response.status_code == 400
    #     assert response.headers["Content-Type"] == "application/json"
    #     assert "should be a string" == json.loads(response.data)['error']['parcel_description']
    #
    # def test_get_all_parcels(self):
    #     post_order = dict(parcel_location="jinja", parcel_destination="manafwa", parcel_weight=24.7,
    #                       parcel_description="apples", user_id=1, status="pending")
    #     post_order2 = dict(parcel_location="kisumu", parcel_destination="mbale", parcel_weight=78,
    #                        parcel_description="eggs", user_id=2, status="cancelled")
    #     response = self.app.post('/api/v1/parcel', json=post_order,headers={"token": self.user_generated_token})
    #     response2 = self.app.post('/api/v1/parcel', json=post_order2,headers={"token": self.user_generated_token} )
    #     response3 = self.app.get('/api/v1/parcel', headers={"token": self.user_generated_token})
    #     assert response3.status_code == 200
    #     assert response3.headers["Content-Type"] == "application/json"
    #     assert "jinja" and "kisumu" in str(response3.data)
    #
    # def test_get_parcel_by_id(self):
    #     response = self.app.post('/api/v1/parcel',headers={"token": self.user_generated_token} )
    #     response1 = self.app.get('/api/v1/parcel/1' ,headers={"token": self.user_generated_token})
    #     response2 = self.app.get('api/v1/parcel/w',headers={"token": self.user_generated_token} )
    #     assert response1.status_code == 200
    #     assert response2.status_code == 404
    #     assert response1.headers["Content-Type"] == "application/json"
    #
    # def test_parcel_by_user_id(self):
    #     response = self.app.post('/api/v1/parcel',headers={"token": self.user_generated_token})
    #     response1 = self.app.get('/api/v1/users/1/parcel',headers={"token": self.user_generated_token})
    #     response2 = self.app.get('/api/v1/users/w/parcel',headers={"token": self.user_generated_token})
    #     assert response1.status_code == 200
    #     assert response2.status_code == 404
    #     assert response1.headers["Content-Type"] == "application/json"
    #
    # def test_cancel_parcel(self):
    #     response = self.app.post('/api/v1/parcel',headers={"token": self.user_generated_token})
    #     response2 = self.app.get('/api/v1/parcel/h/cancel', headers={"token": self.user_generated_token})
    #     assert response2.status_code == 404
    #
    #

