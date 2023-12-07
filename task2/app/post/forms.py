from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,FileField, SelectField

class PostForm(FlaskForm):
    title = StringField('Post Title')
    text = StringField('Post Text')
    image = FileField('Profile Image')
    enabled = BooleanField('Enabled', default=True)
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Create Post')

class CategoryForm(FlaskForm):
    name = StringField('Category Title')
    submit = SubmitField('Add Category')