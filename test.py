from unittest import TestCase
from app import app
from flask import session
from models import db, connect_db, User


class BloglyTest(TestCase):
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
            self.assertIn(
                'https://bcdcog.com/wp-content/uploads/2016/05/profile-default-02.png', html)

            new_user = db.session.query(User).order_by(User.id.desc()).first()

            db.session.delete(new_user)
            db.session.commit()


    def test_valid_user_profile(self):
        with app.test_client() as client:
            resp = client.get("/user/1")
            html = resp.get_data(as_text=True)

            user = User.query.get(1)
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
