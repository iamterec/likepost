from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from extensions import db
from models.post import Post
from models.user import User


class PostsResource(Resource):
    '''route: /posts'''
    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str)
    parser.add_argument("content", type=str)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        user_identity = get_jwt_identity()
        user = User.query.filter(User.email == user_identity["email"]).first()
        post = Post(title=data["title"], content=data["content"], creator_id=user.id)
        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError:
            print('Users id: ', user.id)
            db.session.rollback()
            return {"error": "Wrong data"}, 422
        return {"post": post.to_dict()}

    def get(self):
        limit = 1000
        posts = Post.query.limit(limit)
        return {"posts": [post.to_dict() for post in posts]}


class OnePostResource(Resource):
    '''route: /posts/<post_id>'''

    def get(self, post_id):
        post = Post.query.get(post_id)
        if post:
            return {"post": post.to_dict()}
        else:
            return {"error": "Post not found."}, 404

    @jwt_required
    def delete(self, post_id):
        user_identity = get_jwt_identity()
        user = User.query.filter(User.email == user_identity["email"]).first()
        post = Post.query.filter(Post.creator_id == user.id).filter(Post.id == post_id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return {"msg": "Post has been deleted"}, 200
        else:
            return {"error": "Post not found"}, 404


class LikeResource(Resource):
    '''route: /posts/<post_id>/likes'''

    @jwt_required
    def put(self, post_id):
        user_identity = get_jwt_identity()
        user = User.query.filter(User.email == user_identity["email"]).first()
        post = Post.query.get(post_id)
        # post = Post.query.filter(Post.id == post_id).first()
        if not post:
            return {"error": "Post not found"}, 404

        if post and (user not in post.liked_by):
                post.liked_by.append(user)
                db.session.commit()
                return {"msg": "Post has been liked by you"}
        else:
            return {"msg": "Post already liked by you"}

    @jwt_required
    def delete(self, post_id):
        user_identity = get_jwt_identity()
        user = User.query.filter(User.email == user_identity["email"]).first()
        post = Post.query.filter(Post.creator_id == user.id).filter(Post.id == post_id).first()
        if not post:
            return {"error": "Post not found"}, 404
        if post and (user in post.liked_by):
            post.liked_by.remove(user)
            db.session.commit()
            return {"msg": "You have canceled your like"}
        else:
            return {"msg": "You didn't like this post"}, 400
