from flask_testing import TestCase
from app import create_app

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = create_app()

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        return app

