from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from declutter.models.users import Users


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
            validate_username,], )

    update_submit = SubmitField('Update')
