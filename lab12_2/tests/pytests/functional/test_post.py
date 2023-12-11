from extensions import db
from app.post.models import Post

def test_home_page(test_client, init_database):
    response = test_client.get('/post')
    assert response.status_code == 200
    assert b"post1" in response.data
    assert b"post2" in response.data
    assert b"post3" in response.data

def test_home_page_post(test_client):
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"post1" not in response.data

def test_get_create_post_page(test_client, init_database):
    response = test_client.get("/post/create")
    assert response.status_code == 200
    assert b'Create a New Post' in response.data

def test_post_create_post_page(test_client):
    response = test_client.post('/post/create', data={
        'title': 'post title',
        'text': 'post text',
        'user_id': 1,
        'category_id': 1
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'post title' in response.data
    assert b'post text' in response.data

    post = db.session.query(Post).filter(Post.title == "post title").first()
    assert post is not None

def test_get_post_page(test_client, init_database):
    response = test_client.get("/post/1")
    assert response.status_code == 200
    assert b"post1 text" in response.data

def test_get_update_post_page(test_client):
    response = test_client.get("/post/1/update")
    assert response.status_code == 200
    assert b"Update Post" in response.data

def test_post_update_post_page(test_client):
    test_post = Post(title="Test Post", text="Test Text", enabled=True)
    db.session.add(test_post)
    db.session.commit()

    response = test_client.post(
        f'/post/{test_post.id}/update',
        data={
            'title': 'Updated Title',
            'text': 'Updated Text',
            'enabled': False,
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Updated Title" in response.data

    updated_post = db.session.query(Post).filter(Post.id == test_post.id).first()
    assert updated_post.title == 'Updated Title'
    assert updated_post.text == 'Updated Text'
    assert updated_post.enabled is False

def test_get_delete_post_page(test_client, init_database):
    test_post = Post(title="Test Post", text="Test Text", enabled=True)
    db.session.add(test_post)
    db.session.commit()

    response = test_client.get(f"/post/{test_post.id}/delete")
    assert response.status_code == 302
    assert b"Test Post" not in response.data

    deleted_post = db.session.query(Post).filter(Post.id == test_post.id).first()
    assert deleted_post is None