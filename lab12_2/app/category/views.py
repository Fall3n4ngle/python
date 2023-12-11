from flask import Blueprint, render_template, redirect, url_for
from extensions import db
from .models import Category
from .forms import CategoryForm

categoryBp = Blueprint('category', __name__, template_folder="templates/category")

@categoryBp.route('/', methods=['GET'])
def categories():
    categories_list = db.session.query(Category).all()
    return render_template("categories.html", categories_list=categories_list)

@categoryBp.route('/<int:id>', methods=['GET'])
def category(id):
    category = db.session.query(Category).filter(Category.id == id).first()
    return render_template("category.html", category=category)

@categoryBp.route('/create', methods=['GET', 'POST'])
def createCategory():
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data

        newCategory = Category(name=name)
        db.session.add(newCategory)
        db.session.commit()

        return redirect(url_for('category.categories'))
    
    return render_template("createCategory.html", form=form)

@categoryBp.route("/<int:id>/delete")
def deletePost(id):
    category = db.session.query(Category).filter(Category.id == id).first()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("category.categories"))

@categoryBp.route('/<int:id>/update', methods=["POST", "GET"])
def updateCategory(id):
    form = CategoryForm()
    category = db.session.query(Category).filter(Category.id == id).first()

    if form.validate_on_submit():
        name = form.name.data
        category.name = name

        db.session.commit()

        return redirect(url_for('category.category'), id=category.id)

    return render_template("updateCategory.html", form=form, category_id=category.id)