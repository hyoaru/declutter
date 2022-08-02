from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from declutter.database import bcrypt
from declutter.blueprints.models.users import Users

class UpdateEmail(FlaskForm):
    # Custom validators
    def validate_email(self, user_email):
        if user_email.data != current_user.user_email:
            if Users.query.filter_by(user_email = user_email.data).first():
                raise ValidationError(message = 'Email already exists')
        else:
            raise ValidationError(message = 'You are already using that email')

    def password_confirm(self, user_password):
        if not bcrypt.check_password_hash(pw_hash = current_user.user_password, password = user_password.data):
            raise ValidationError(message = 'Incorrect password')

    # Forms
    user_email = StringField(
        'Desired email',
        validators = [
            DataRequired(message = 'Must provide an email'),
            Email(),
            Length(max = 200, message = 'Email must be under 200 characters'),
            validate_email
        ]
    )

    user_password_confirm = PasswordField(
        'Confirm password',
        validators = [
            DataRequired(message = 'Must provide a password confirmation'),
            password_confirm
        ]
    )

    update_submit = SubmitField('Update')

class UpdateUsername(FlaskForm):
    # Custom validators
    def validate_username(self, user_username):
        if user_username.data != current_user.user_username:
            if Users.query.filter_by(user_username = user_username.data).first():
                raise ValidationError(message = 'Username already exists')
        else:
            raise ValidationError(message = 'You are already using that username')

    # Forms
    user_username = StringField(
        'Desired username',
        validators = [
            DataRequired(message = 'Must provide a username'),
            Length(min = 3, max = 40, message = 'Username must be between 3 and 40 characters long'),
            validate_username
        ]
    )

    update_submit = SubmitField('Update')

class UpdatePassword(FlaskForm):
    # Custom validators
    def validate_password(self, user_password_current):
        if not bcrypt.check_password_hash(pw_hash = current_user.user_password, password = user_password_current.data):
            raise ValidationError(message = 'Incorrect password')

    # Forms
    user_password_current = PasswordField(
        'Current password',
        validators = [
            DataRequired(message = 'Must provide current password'),
            validate_password
        ]
    )

    user_password_new = PasswordField(
        'New password',
        validators = [
            DataRequired(message = 'Must provide a new password'),
            Length(min = 8, max = 40, message = 'Password must be between 8 and 40 characters long')
        ]
    )

    user_password_new_confirm = PasswordField(
        'Confirm new password',
        validators = [
            DataRequired(message = 'Must provide a password confirmation'),
            EqualTo(fieldname = 'user_password_new', message = 'Password does not match')
        ]
    )

    update_submit = SubmitField('Update')