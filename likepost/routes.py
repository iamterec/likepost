from resourses.users import Registration


def connect_resources(api):
    api.add_resource(Registration, "/users")
