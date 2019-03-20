import pytest

SIGNUP_ENDPOINT = "/users"
LOGIN_ENDPOINT = "/users/login"


class TestSignUp:

    def test_big_data(self, client):
        user_data = {"password": "somepassword",
                     "email": "somemail@mail.com",
                     "username": "a"*100}
        resp = client.post(SIGNUP_ENDPOINT, data=user_data)
        assert resp.status_code == 403

    def test_invalid_data(self, client):
        user_data = {"password": "somepassword",
                     "email": "some_text_that_is_not_email"}
        resp = client.post(SIGNUP_ENDPOINT, data=user_data)
        assert resp.status_code == 422

    def test_missed_field(self, client):
        user_data = {"password": "somepassword",
                     "email": "username@mail.com"}
        resp = client.post(SIGNUP_ENDPOINT, data=user_data)
        assert resp.status_code == 200
        resp = client.delete(SIGNUP_ENDPOINT, data=user_data)
        assert resp.status_code == 200


@pytest.yield_fixture(scope='function')
def access_token(client, test_user_data):
    resp = client.post(LOGIN_ENDPOINT, data=test_user_data)
    assert resp.status_code == 200
    access_token = resp.json["access_token"]
    yield access_token


class TestLogin:
    def test_wrong_password(self, client, test_user_data):
        data = test_user_data.copy()
        data["password"] += "ha-ha-ha(evil voice)"
        resp = client.post(LOGIN_ENDPOINT, data=data)
        assert 400 <= resp.status_code < 500

    def test_wrong_email(self, client, test_user_data):
        data = test_user_data.copy()
        data["email"] += "no_more_mails"
        resp = client.post(LOGIN_ENDPOINT, data=data)
        assert 400 <= resp.status_code < 500

    def test_success(self, client, test_user_data):
        resp = client.post(LOGIN_ENDPOINT, data=test_user_data)
        assert resp.status_code == 200
