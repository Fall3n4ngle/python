from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class FeedbackForm(FlaskForm):
    name = StringField('Your name')
    message = StringField('Your message')
    submit = SubmitField('Add feedback')