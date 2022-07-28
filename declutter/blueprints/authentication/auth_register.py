from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    user_email = StringField(
        'Email',
        validators = [
            DataRequired(message = 'Must provide an email.'),
            Email()
        ]
    )

    user_username = StringField(
        'Username',
        validators = [
            DataRequired(message = 'Must provide a username'), 
            Length(min = 3, max = 20, message = 'Username must be between 3 and 20 characters long')
        ]
    )

    user_password = PasswordField(
        'Password',
        validators = [
            DataRequired(message = 'Must provide a password.'),
            Length(min = 8, max = 40, message = 'Password must be between 8 and 40 characters long')
        ]
    )

    user_password_confirm = PasswordField(
        'Confirm password',
        validators = [
            DataRequired(message = 'Must provide a password confirmation.'),
            EqualTo(fieldname = 'user_password', message = 'Password does not match')
        ]
    )

    registration_submit = SubmitField('Sign up')