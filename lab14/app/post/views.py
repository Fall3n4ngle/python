from flask import Blueprint, render_template, redirect, url_for, request
from .models import Post
from .forms import PostForm
from extensions import db
from app.utils import save_uploaded_image
from flask_login import current_user
from app.category.models import Category

postBp = Blueprint('post', __name__, template_folder="templates/post")

@postBp.route('/', methods=['GET'])
def posts():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    post_pagination = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=per_page)
    post_list = post_pagination.items

    return render_template("posts.html", post_list=post_list, pagination=post_pagination)

@postBp.route('/<int:id>', methods=['GET'])
def post(id):
    post = db.session.query(Post).filter(Post.id == id).first()
    return render_template("post.html", post=post)
    

@postBp.route('/create', methods=['GET', 'POST'])
def createPost():
    form = PostForm()
    categories = db.session.query(Category).all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        image = form.image.data
        enabled = form.enabled.data
        user_id = current_user.get_id()
        category_id = form.category.data

        file_url=None
        if image:
            file_url = save_uploaded_image(image)

        newPost = Post(title=title, text=text, image=file_url, enabled=enabled, user_id=user_id, category_id=category_id)
        db.session.add(newPost)
        db.session.commit()

        return redirect(url_for('post.posts'))

    return render_template("createPost.html", form=form, categories=categories)

@postBp.route("/<int:id>/delete")
def deletePost(id):
    post = db.session.query(Post).filter(Post.id == id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("post.posts"))

@postBp.route('/<int:id>/update', methods=["POST", "GET"])
def updatePost(id):
    form = PostForm()
    post = db.session.query(Post).filter(Post.id == id).first()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        image = form.image.data
        post.enabled = form.enabled.data

        if image:
            post.image = save_uploaded_image(image)

        db.session.commit()

        return redirect(url_for('post.post'), id=post.id)

    return render_template("updatePost.html", form=form, post_id=post.id)