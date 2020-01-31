"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


def connect_db(app):
    """Connect to database. """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(15),
                           nullable=False)
    last_name = db.Column(db.String(25),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default='https://bcdcog.com/wp-content/uploads/2016/05/profile-default-02.png')

    def __repr__(self):
        """ Show info about user."""

        user = self
        return f"<User {user.id}: {user.first_name} {user.last_name}>"

    def edit_user(self, first_name, last_name, image_url):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    posts = db.relationship('Post', backref="user")


class Post(db.Model):
    """Post. """
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))


class Tag(db.Model):
    """Tag. """
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(20),
                     nullable=False)

    posts = db.relationship('Post',
                            secondary='post_tags',
                            backref='tags')


class PostTag(db.Model):
    """PostTag. """
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
