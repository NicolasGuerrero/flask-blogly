"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
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
    image_url = db.Column(db.String(512),
                          nullable=False,
                          default='https://static1.squarespace.com/static/54b7b93ce4b0a3e130d5d232/54e20ebce4b014cdbc3fd71b/5a992947e2c48320418ae5e0/1519987239570/icon.png')

    def __repr__(self):
        """ Show info about user."""

        user = self
        return f"<User {user.id}: {user.first_name} {user.last_name}>"

    def edit_user(self, first_name, last_name, image_url):
        self.first_name=first_name
        self.last_name=last_name
        self.image_url=image_url
