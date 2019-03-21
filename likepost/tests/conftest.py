import pytest
from app import create_app
from tests.test_users import LOGIN_ENDPOINT


@pytest.yield_fixture(scope='session')
def app():
    params = {
        'DEBUG': False,
        'TESTING': True,
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session")
def test_user_data():
    user_data = {"email": "temp_user@mail.com",
                 "password": "temp_password",
                 "username": "some_user"}
    return user_data


@pytest.yield_fixture(scope='function')
def client(app):
    yield app.test_client()


@pytest.yield_fixture(scope="session", autouse=True)
def client_with_user(app, test_user_data):
    user_data = test_user_data
    client = app.test_client()
    resp = client.post("/users", data=user_data)  # create test user
    assert resp.status_code == 200
    yield
    # get access_token
    resp = client.post(LOGIN_ENDPOINT, data=test_user_data)
    assert resp.status_code == 200
    access_token = resp.json["access_token"]
    headers = {"Authorization": "Bearer " + access_token}
    # delete user
    resp = client.delete("/users", data=user_data, headers=headers)
    assert resp.status_code == 200


@pytest.yield_fixture(scope='function')
def access_token(client, test_user_data):
    resp = client.post(LOGIN_ENDPOINT, data=test_user_data)
    assert resp.status_code == 200
    access_token = resp.json["access_token"]
    yield access_token
