from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from main_app.models import User
from wtforms import ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username',
                             validators=[DataRequired(message='Username is required')])
    email = StringField('Email', 
                        validators=[DataRequired(message='Email is required'),Email(message='Please fill the correct email')])
    password = PasswordField('Password', 
                            validators=[DataRequired(message='Password is required')])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(message='Username is required')])
    email = StringField('Email', 
                        validators=[DataRequired(message='Email is required'),Email(message='Please fill the correct email')])
    password = PasswordField('Password', 
                            validators=[DataRequired(message='Password required'),EqualTo('pass_confirm', message="Passwords must match")])
    pass_confirm = PasswordField('Confirm Password', 
                                validators=[DataRequired(message='Please Confirm your password')])
    submit = SubmitField('SignUp')
    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Your username has been registered already!') 
    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Your email has been registered already!') 

