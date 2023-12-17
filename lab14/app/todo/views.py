from flask import Blueprint
from flask import redirect, url_for, render_template
from .forms import TaskForm
from app.models.todo import Todo
from extensions import db

todo = Blueprint('todo', __name__, template_folder="templates/todo")

@todo.route('/', methods=['GET', 'POST'])
def todoRoute():
    form = TaskForm()
    todo_list = db.session.query(Todo).all()

    if form.validate_on_submit():
        title = form.title.data
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("todo.todoRoute"))

    return render_template('todo.html', todo_list=todo_list, form=form)

@todo.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo.todoRoute"))
 
@todo.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo.todoRoute"))