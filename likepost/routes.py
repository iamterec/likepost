from resourses.users import Signup, Login


def connect_resources(api):
    api.add_resource(Signup, "/users")
    api.add_resource(Login, "/users/login")
