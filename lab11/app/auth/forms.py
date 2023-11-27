from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=14), 
                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must only have letters, numbers, dots or underscores') 
                                        ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=14), 
                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must only have letters, numbers, dots or underscores') 
                                        ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = FileField('Profile Image')
    about_me = StringField('About Me')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])