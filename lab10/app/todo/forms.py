from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class TaskForm(FlaskForm):
    title = StringField('Task Title')
    submit = SubmitField('Add Task')