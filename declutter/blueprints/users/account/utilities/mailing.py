from typing import Type
from flask import url_for
from flask_mail import Message

# App imports
from declutter.utilities.backend import mail

# Database models
from declutter.models.users import Users


def send_email_verification_request(user: Type[Users]) -> None:
    """Sends an email for email verification."""

    email_verification_token = user.get_token()
    message = Message(
        subject = 'Email Verification Request', sender = 'declutthoughts@gmail.com', recipients = [user.user_email],
        body = (
            "To verify your email, visit the following link:\n"
            f"{url_for('users_account.email_verification', token = email_verification_token, _external = True)}\n"
            "If you did not make this request, simply ignore this email and no changes will be made."), )
    
    mail.send(message)