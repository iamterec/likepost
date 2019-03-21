from extensions import db

association_table = db.Table("likes", db.Model.metadata,
                             db.Column("post", db.Integer, db.ForeignKey("posts.id")),
                             db.Column("user", db.Integer, db.ForeignKey("users.id")))

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String)
    creation_date = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                           nullable=False)
    liked_by = db.relationship("User", secondary=association_table,
                                 back_populates="liked_posts")

    def to_dict(self, creation_date=False):
        post_dict = {}
        post_dict["id"] = self.id
        post_dict["title"] = self.title
        post_dict["content"] = self.content
        post_dict["creator_id"] = self.creator_id
        if creation_date:
            post_dict["creation_date"] = self.creation_date
        return post_dict
