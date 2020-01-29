"""Blogly application."""

from flask import Flask, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)


@app.route("/")
def start():
    return redirect("/users")

@app.route("/users")
def show_user_list():
    # render user list and add user button

@app.route("/users/new")
    # render new user form 

@app.route("users/new", methods=["POST"])
    # create new user in database from form inputs
    # redirect to user list '/users'

@app.route("user/<int:user_id>")
    # render user_id detail page
    # button to edit or delete

@app.route("user/<int:user_id>/edit")
    # render the edit form
    # 

@app.route("user/<int:user_id>/edit", methods=["POST"])
    # edit the user in the database
    # redirect to all users list '/users'

@app.route("user/<int:user_id>/delete", methods=["POST"])
    # delete the user in the database
    # redirect to '/users'