SIGNUP_ENDPOINT = "/users"
LOGIN_ENDPOINT = "/users/login"
DELETE_ENDPOINT = "/users/me"


class TestSignUp:
    def test_big_data(self, client):
        '''Try to signup user with too long username.'''
        user_data = {"password": "somepassword",
                     "email": "somemail@mail.com",
                     "username": "a"*100}
        resp = client.post(SIGNUP_ENDPOINT, data=user_data)
        assert resp.status_code == 403

    def test_invalid_data(self, client):
        '''Try to signup user with wrong email field.'''
        user_data = {"password": "somepassword",
                     "email": "some_text_that_is_not_email"}
        resp = client.post(SIGNUP_ENDPOINT, data=user_data)
        assert resp.status_code == 422

    def test_missed_field(self, client):
        '''Sign up user with optional username field.'''
        user_data = {"password": "somepassword",
                     "email": "username@mail.com"}
        resp = client.post(SIGNUP_ENDPOINT, data=user_data)
        assert resp.status_code == 200
        # get access_token and delete user
        resp = client.post(LOGIN_ENDPOINT, data=user_data)
        assert resp.status_code == 200
        access_token = resp.json["access_token"]
        headers = {"Authorization": "Bearer " + access_token}
        resp = client.delete(DELETE_ENDPOINT, data=user_data, headers=headers)
        assert resp.status_code == 200


class TestLogin:
    def test_wrong_password(self, client, test_user_data):
        '''Try to login user with wrong password.'''
        data = test_user_data.copy()
        data["password"] += "ha-ha-ha(evil voice)"
        resp = client.post(LOGIN_ENDPOINT, data=data)
        assert 400 <= resp.status_code < 500

    def test_wrong_email(self, client, test_user_data):
        '''Try to login user with wrong email.'''
        data = test_user_data.copy()
        data["email"] += "no_more_mails"
        resp = client.post(LOGIN_ENDPOINT, data=data)
        assert 400 <= resp.status_code < 500

    def test_success(self, client, test_user_data):
        '''Sign up existing user.'''
        resp = client.post(LOGIN_ENDPOINT, data=test_user_data)
        assert resp.status_code == 200
