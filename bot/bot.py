import json
import requests
import random
import string
from faker import Faker
from json.decoder import JSONDecodeError
from user import User

GET_POSTS_URL = "http://api:8000/posts"

class Bot:
    def __init__(self, config):
        self.__dict__.update(config)
        self.faker = Faker()
        self.old_users = get_users()
        self.new_users = []


    def write_users(self):
        with open("users.json", "w") as file:
            new_users = [user.to_dict() for user in self.new_users]
            old_users = [user.to_dict() for user in self.old_users]
            json.dump(old_users + new_users, file, indent=4)

    def generate_user(self):
        rand_chars = get_random_string(3, only_lowercase=True)
        name = self.faker.name()
        email = name.replace(" ", "").lower() + rand_chars + "@mail.com"
        password = get_random_string(12)
        return User({"username": name, "email": email, "password": password})

    def generate_post(self):
        title = self.faker.sentence()
        content = self.faker.paragraph(random.randint(5, 15))
        return {"title": title, "content": content}

    def _signup_users(self):
        print("Sign up users({}): ".format(self.number_of_users), end="")
        for _ in range(self.number_of_users):
            user = self.generate_user()
            result = user.signup()
            if result:
                self.new_users.append(user)
                print("+", end="")
            else:
                print("\nUnable to signup user {}.".format(user.username), end="")
        print()

    def _delete_new_users(self):
        for _ in range(len(self.new_users)):
            user = self.new_users.pop()
            user.delete(silent=False)

    def _create_posts(self):
        print("Creating posts for every new user: ", end="")
        for user in self.new_users:
            number_of_posts = random.randint(1, self.max_posts_per_user)
            for _ in range(number_of_posts):
                post = self.generate_post()
                result = user.create_post(post)
                if result:
                    print("+", end="")
        print()

    def get_all_posts(self):
        resp = requests.get(GET_POSTS_URL)
        return resp.json()["posts"] if resp.status_code == 200 else []

    def _like_posts(self):
        posts = self.get_all_posts()
        if not posts:
            print("No post comes for likes")
            return False
        print("Like posts for every new user: ", end="")
        for user in self.new_users:
            for _ in range(random.randint(1, self.max_likes_per_user)):
                post = random.choice(posts)
                result = user.like_post(post)
                if result:
                    print("+", end="")
        print()


    def create_activity(self):
        self._signup_users()
        self._create_posts()
        self._like_posts()

        resp = input("Should I delete created users from the service? (y/n):")
        if resp in ["Y", "y", "yes", "yes"]:
            self._delete_new_users()
        else:
            self.write_users()


def get_users():
    with open("users.json", "r") as file:
        try:
            users = json.load(file)
        except JSONDecodeError:
            return []
    return [User(user) for user in users]


def get_random_string(length, only_lowercase=False):
    letters = string.ascii_lowercase if only_lowercase else string.ascii_letters
    return "".join(random.choice(letters + string.digits) for _ in range(length))


def read_config(path):
    with open(path, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    config = read_config("config.json")
    bot = Bot(config)
    bot.create_activity()
