from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    user_username = StringField(
        'Username',
        validators = [
            DataRequired(), 
            Length(min = 3, max = 20)
        ]
    )

    user_password = PasswordField(
        'Password',
        validators = [
            DataRequired()
        ]
    )

    login_remember = BooleanField('Remember me')

    login_submit = SubmitField('Log in')