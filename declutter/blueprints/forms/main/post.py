from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from declutter.database import bcrypt
from declutter.blueprints.models.users import Users


class PostCreate(FlaskForm):
    post_title = StringField(
        'Title',
        validators = [
            DataRequired(message = 'Must provide a title'),
            Length(max = 100, message = 'Title must be under 100 characters')
        ]
    )

    post_content = TextAreaField(
        'Content',
        validators = [
            DataRequired(message = 'Must provide content'),
            Length(max = 1500, message = 'Content must be under 1500 characters')
        ]
    )

    post_submit = SubmitField('Post')