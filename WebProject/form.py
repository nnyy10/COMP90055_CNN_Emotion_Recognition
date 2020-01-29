from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from model import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Email is null'), Email()])
    username = StringField('Username', validators=[DataRequired('Username is null')])
    password = PasswordField('Password', validators=[DataRequired('Password is null')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired('Passwords are different'), EqualTo('password')])
    submit = SubmitField('Register')


    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')
    #
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')



