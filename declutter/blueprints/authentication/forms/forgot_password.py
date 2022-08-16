from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError

# Database models
from declutter.models.users import Users

class ForgotPassword(FlaskForm):

    # Custom validators
    def validate_email(self, user_email):
        if Users.query.filter_by(user_email = user_email.data).first() is None:
            raise ValidationError(message = 'User with that email does not exist')

    def validate_username(self, user_username):
        if Users.query.filter_by(user_username = user_username.data).first() is None:
            raise ValidationError(message = 'User with that username does not exist')

    def validate_input(self, input):
        self.validate_email(input) if '@' in input.data else self.validate_username(input)

    # Forms
    user_input = StringField(
        'Input',
        validators = [DataRequired(message = 'Must provide an input'), validate_input,], )

    forgot_password_mode = RadioField(
        'test',
        choices = [('by_email', 'Email'), ('by_username', 'Username')], default = 'by_email', 
        validators = [DataRequired(message = 'Must provide a mode')], )

    forgot_password_submit = SubmitField('Submit')