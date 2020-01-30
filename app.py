"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)


@app.route("/")
def start():
    return redirect("/users")


@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route("/users/new")
def show_new_form():
    return render_template('new_user.html')


@app.route("/users/new", methods=["POST"])
def submit_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/user/<int:user_id>")
def show_profile(user_id):
    # button to edit or delete
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@app.route("/user/<int:user_id>/edit")
def show_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route("/user/<int:user_id>/edit", methods=["POST"])
def submit_edit(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User.query.get_or_404(user_id)
    # user = User.query.get(user_id)
    user.edit_user(first_name=first_name,
                   last_name=last_name,
                   image_url=image_url)

    db.session.commit()

    return redirect("/users")


@app.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

