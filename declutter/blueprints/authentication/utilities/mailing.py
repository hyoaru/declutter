from typing import Type
from flask import url_for
from flask_mail import Message

# App imports
from declutter.utilities.backend import mail

# Database models
from declutter.models.users import Users


def send_reset_password_email(user: Type[Users]) -> None:
    """Sends an email for password reset request."""

    reset_token = user.get_reset_token()
    message = Message(
        subject = 'Password Reset Request', sender = 'declutthoughts@gmail.com', recipients = [user.user_email],
        body = (
            "To reset your password, visit the following link:\n"
            f"{url_for('authentication.reset_password', reset_token = reset_token, _external = True)}\n"
            "If you did not make this request, simply ignore this email and no changes will be made."), )
    
    mail.send(message)