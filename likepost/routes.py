from resourses.users import Signup, Login, UserMe
from resourses.posts import PostsResource, OnePostResource, LikeResource


def connect_resources(api):
    api.add_resource(Signup, "/users")
    api.add_resource(Login, "/users/login")
    api.add_resource(UserMe, "/users/me")
    api.add_resource(PostsResource, "/posts")
    api.add_resource(OnePostResource, "/posts/<int:post_id>")
    api.add_resource(LikeResource, "/posts/<int:post_id>/likes")
