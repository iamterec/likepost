import requests


class Endpoints:
    base_url = "http://api:8000"
    signup_url = base_url + "/users"
    login_url = base_url + "/users/login"
    delete_user_url = base_url + "/users/me"
    create_post_url = base_url + "/posts"
    like_post_url = base_url + "/posts/{}/likes"


class User(Endpoints):
    def __init__(self, user):
        self.email = user["email"]
        self.password = user["password"]
        self.username = user.get("username", None)

    def signup(self):
        resp = requests.post(self.signup_url, data=self.to_dict())
        return True if resp.status_code == 200 else False

    def _login(self):
        resp = requests.post(self.login_url, data=self.to_dict())
        if resp.status_code == 200:
            access_token = resp.json()["access_token"]
            self.access_token = access_token
            return access_token
        else:
            print("\nCann't login user {}".format(self.username))

    def get_access_token(self, update=False):
        if update:
            access_token = self._login()
            return access_token
        else:
            return getattr(self, "access_token", False) or self._login()

    def delete(self, silent=True):
        access_token = self.get_access_token()
        headers = {"Authorization": "Bearer " + access_token}
        resp = requests.delete(self.delete_user_url, data=self.to_dict(),
                               headers=headers)
        if not silent:
            if resp.status_code == 200:
                print("User {} has been deleted".format(self.username))
            else:
                print("Cann't delete user {}".format(self.username))
        return True if resp.status_code == 200 else False

    def create_post(self, post):
        access_token = self.get_access_token()
        headers = {"Authorization": "Bearer " + access_token}
        resp = requests.post(self.create_post_url, data=post, headers=headers)
        return True if resp.status_code == 200 else False

    def like_post(self, post):
        access_token = self.get_access_token()
        headers = {"Authorization": "Bearer " + access_token}
        resp = requests.put(self.like_post_url.format(post["id"]), headers=headers)
        return True if resp.status_code == 200 else False

    def to_dict(self):
        return {"email": self.email,
                "password": self.password,
                "username": self.username}
