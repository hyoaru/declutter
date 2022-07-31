from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from declutter.blueprints.models.users import Users

class RegistrationForm(FlaskForm):

    # Custom validators
    def validate_email(self, user_email):
        if Users.query.filter_by(user_email = user_email.data).first():
            raise ValidationError(message = 'Email already exists.')

    def valdiate_username(self, user_username):
        if Users.query.filter_by(user_username = user_username.data).first():
            raise ValidationError('Username is already taken.')

    # Forms
    user_email = StringField(
        'Email',
        validators = [
            DataRequired(message = 'Must provide an email.'),
            Email(),
            Length(max = 200, message = 'Email must be under 200 characters.'),
            validate_email

        ]
    )

    user_username = StringField(
        'Username',
        validators = [
            DataRequired(message = 'Must provide a username.'), 
            Length(min = 3, max = 40, message = 'Username must be between 3 and 40 characters long.'),
            valdiate_username
        ]
    )

    user_password = PasswordField(
        'Password',
        validators = [
            DataRequired(message = 'Must provide a password.'),
            Length(min = 8, max = 40, message = 'Password must be between 8 and 40 characters long.')
        ]
    )

    user_password_confirm = PasswordField(
        'Confirm password',
        validators = [
            DataRequired(message = 'Must provide a password confirmation.'),
            EqualTo(fieldname = 'user_password', message = 'Password does not match.')
        ]
    )

    registration_submit = SubmitField('Sign up')

