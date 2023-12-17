from .base import BaseTestCase
from extensions import db
from app.auth.models import User

class AuthTests(BaseTestCase):
    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_page_loads(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>Register</h2>', response.data)

    def test_login_page_loads(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>Login</h2>', response.data)

    def test_register_user(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        response = self.client.post('/auth/register', data=form_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account was created for testuser!', response.data)
        self.assertTrue(User.query.filter_by(username='testuser').first())

    def test_login_user(self):
        self.test_register_user()

        form_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'remember': False
        }
        response = self.client.post('/auth/login', data=form_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged in!', response.data)

    def test_logout_user(self):
        self.test_login_user()

        response = self.client.get('/auth/logout', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)

    def test_update_account(self):
        self.test_login_user()

        form_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'image_file': 'test.jpg',
            'about_me': 'New about me text'
        }
        response = self.client.post('/auth/update_account', data=form_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account updated successfully', response.data)

        updated_user = User.query.filter_by(username='newusername').first()
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.email, 'newemail@example.com')
        self.assertEqual(updated_user.image_file, 'test.jpg')
        self.assertEqual(updated_user.about_me, 'New about me text')

    def test_change_password(self):
        self.test_login_user()

        form_data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword',
            'confirm_new_password': 'newpassword'
        }
        response = self.client.post('/auth/change_password', data=form_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password changed successfully', response.data)

        updated_user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(updated_user)
        self.assertTrue(updated_user.check_password('newpassword'))
            
            


