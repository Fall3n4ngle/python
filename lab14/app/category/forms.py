from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class CategoryForm(FlaskForm):
    name = StringField('Category Title')
    submit = SubmitField('Update Category')