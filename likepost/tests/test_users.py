class TestRegistration:

    def test_big_data(self, client):
        user_data = {"password": "somepassword",
                     "email": "somemail@mail.com",
                     "username": "a"*100}
        resp = client.post("/users", data=user_data)
        assert resp.status_code == 403

    def test_invalid_data(self, client):
        user_data = {"password": "somepassword",
                     "email": "some_text_that_is_not_email"}
        resp = client.post("/users", data=user_data)
        assert resp.status_code == 422
