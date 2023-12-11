from app.post.models import Post

def test_new_post():
    post = Post(
        title="post1", text="post1 text", user_id=1, category_id=1
    )

    assert post.title == "post1"
    assert post.text == "post1 text"
    assert post.user_id == 1
    assert post.category_id == 1

def test_update_post():
    post = Post(
        title="post1", text="post1 text", user_id=1, category_id=1
    )

    post.title = "post2"
    post.text = "post2 text"

    assert post.title == "post2"
    assert post.text == "post2 text"
    assert post.user_id == 1
    assert post.category_id == 1

