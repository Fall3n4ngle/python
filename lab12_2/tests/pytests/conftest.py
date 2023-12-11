import pytest

from app import create_app
from extensions import db
from app.post.models import Post
from app.category.models import Category

@pytest.fixture(scope='module')
def new_user():
    post = Post(title="post1", text="post1 text", user_id=1, category_id=1)
    return post


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()

    category1 = Category(name="category1")
    category2 = Category(name="category2")

    db.session.add(category1)
    db.session.add(category2)

    db.session.commit()

    post1 = Post(
        title="post1", text="post1 text", user_id=1, category_id=category1.id
    )
    post2 = Post(
        title="post2", text="post2 text", user_id=1, category_id=category2.id
    )
    post3 = Post(
        title="post3", text="post3 text", user_id=2, category_id=category1.id
    )

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)

    db.session.commit()

    yield

    db.drop_all()

@pytest.fixture(scope='module')
def cli_test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    runner = flask_app.test_cli_runner()

    yield runner
