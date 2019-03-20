from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, email, username=None):
        self.email = email
        self.username = username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        user_dict = {}
        user_dict["id"] = self.id
        user_dict["email"] = self.email
        user_dict["username"] = self.username
        return user_dict
