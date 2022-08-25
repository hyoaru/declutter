from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from declutter.utilities.backend import bcrypt
from declutter.models.users import Users


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
            validate_email,], )

    user_password_confirm = PasswordField(
        'Confirm password',
        validators = [
            DataRequired(message = 'Must provide a password confirmation'),
            password_confirm,], )

    update_submit = SubmitField('Update')
