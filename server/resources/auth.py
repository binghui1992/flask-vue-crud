from flask_restful import Resource
from flask import request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin


login_manager = LoginManager()


# TODO, replace memory database with real database
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.email}>"


users = [
    User("1", "email-1", "password-1"),
    User("2", "email-2", "password-2"),
    User("3", "email-3", "password-3"),
]


@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if str(user.id) == user_id:
            return user
    return None


class Login(Resource):
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")
        for user in users:
            if user.email == email and user.password == password:
                login_user(user)
                return {"message": "Logged in successfully."}, 200
        return {"message": "Invalid email or password."}, 401


class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {"message": "Logged out successfully."}, 200
