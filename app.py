"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag
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

@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def submit_new_post(user_id):
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title,
                content=content,
                user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/user/{user_id}')


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post.html', post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_post_edit(post_id):
    title = request.form['title']
    content = request.form['content']
    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    #How to handle time-stamp at edit??
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/user/{user_id}')


@app.route("/tags")
def show_tags():
    tags = Tag.query.all()

    return render_template('tags.html',tags=tags)


@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tag_detail.html', posts=posts, tag=tag)


@app.route("/tags/new")
def new_tag_form():
    return render_template('new_tag.html')


@app.route("/tags/new", methods=["POST"])
def submit_new_tag():
    name = request.form['name']
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def submit_tag_edit(tag_id):
    name = request.form['name']
    tag = Tag.query.get_or_404(tag_id)

    tag.name = name
    db.session.commit()

    return redirect('/tags')


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')