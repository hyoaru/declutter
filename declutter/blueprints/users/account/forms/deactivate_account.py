from flask import request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo

# App imports
from declutter.utilities.backend import bcrypt
from declutter.models.users import Users

class DeactivateAccount(FlaskForm):
    
    def get_deactivate_confirmation(self):
        return f'{request.root_url[:-1]}/user/{current_user.user_username}'

    # Custom validators
    def validate_confirmation(self, deactivate_confirmation):
        if deactivate_confirmation.data != self.get_deactivate_confirmation():
            raise ValidationError(message = 'Deactivate confirmation does not match')

    def password_confirm(self, user_password):
        if not bcrypt.check_password_hash(pw_hash = current_user.user_password, password = user_password.data):
            raise ValidationError(message = 'Incorrect password')

    # Forms
    deactivate_confirmation = StringField(
        'Confirm deactivation',
        validators = [DataRequired(message = 'Must provide confirmation'), validate_confirmation,], )

    user_password_confirm = PasswordField(
        'Confirm password',
        validators = [DataRequired(message = 'Must confirm password'), password_confirm,], )

    deactivate_submit = SubmitField('Deactivate')