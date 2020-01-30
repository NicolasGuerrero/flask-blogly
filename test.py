from unittest import TestCase
from app import app
from flask import session
from models import db, connect_db, User, Post


class UserTests(TestCase):
    def test_submit_new_user(self):
        with app.test_client() as client:
            resp = client.post("/users/new",
                               data=dict(
                                   first_name="John",
                                   last_name="Doe",
                                   image_url=""),
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)

            new_user = db.session.query(User).order_by(User.id.desc()).first()

            db.session.delete(new_user)
            db.session.commit()


    def test_valid_user_profile(self):
        with app.test_client() as client:
            resp = client.get("/user/19")
            html = resp.get_data(as_text=True)

            user = User.query.get(19)
            first_name = user.first_name

            self.assertEqual(resp.status_code, 200)
            self.assertIn(first_name, html)

    def test_invalid_user_profile(self):
        with app.test_client() as client:
            resp = client.get("/user/0")

            self.assertEqual(resp.status_code, 404)

    def test_edit_user(self):
        with app.test_client() as client:
            user = User(first_name="Gretchen",
                        last_name="Weiner",
                        image_url='https://bcdcog.com/wp-content/uploads/2016/05/profile-default-02.png')
            db.session.add(user)
            db.session.commit()

            resp = client.post(f'/user/{user.id}/edit',
                               data=dict(
                                   first_name="Holly",
                                   last_name="Williams",
                                   image_url='https://bcdcog.com/wp-content/uploads/2016/05/profile-default-02.png'),
                               follow_redirects=True)

            editted_user = User.query.get(user.id)

            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual("Gretchen", editted_user.first_name)

            db.session.delete(editted_user)
            db.session.commit()

class PostTests(TestCase):
    def setUp(self):
        # db.session.query(Post).delete()
        Post.query.delete()
        # db.session.query(User).delete()
        User.query.delete()
        user = User(first_name="Gretchen",
                        last_name="Weiner",
                        image_url='https://bcdcog.com/wp-content/uploads/2016/05/profile-default-02.png')
        db.session.add(user)
        db.session.commit()
        self.user = user

        post = Post(title="Test Post",
                    content="Test Content.",
                    user_id = self.user.id)
        db.session.add(post)
        db.session.commit()
        self.post = post
         

    def test_submit_new_post(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user.id}/posts/new',
                               data=dict(
                                    title="Test Post",
                                    content="Content of post."),
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # self.assertIn(self.user.first_name, html)
            self.assertIn("Test Post", html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Content.", html)
            

