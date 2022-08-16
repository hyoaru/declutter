from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class ResetPassword(FlaskForm):
    user_password = PasswordField(
        'Password',
        validators = [
            DataRequired(message = 'Must provide a password.'),
            Length(min = 8, max = 40, message = 'Password must be between 8 and 40 characters long.'),], )

    user_password_confirm = PasswordField(
        'Confirm password',
        validators = [
            DataRequired(message = 'Must provide a password confirmation.'),
            EqualTo(fieldname = 'user_password', message = 'Password does not match.'),], )

    reset_password_submit = SubmitField('Confirm')

