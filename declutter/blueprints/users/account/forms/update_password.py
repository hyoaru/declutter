from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from declutter.utilities.backend import bcrypt
from declutter.models.users import Users


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
            validate_password,], )

    user_password_new = PasswordField(
        'New password',
        validators = [
            DataRequired(message = 'Must provide a new password'),
            Length(min = 8, max = 40, message = 'Password must be between 8 and 40 characters long'),], )

    user_password_new_confirm = PasswordField(
        'Confirm new password',
        validators = [
            DataRequired(message = 'Must provide a password confirmation'),
            EqualTo(fieldname = 'user_password_new', message = 'Password does not match'),], )

    update_submit = SubmitField('Update')