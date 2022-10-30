import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """App configurations."""
    
    # General
    SECRET_KEY = os.getenv("SECRET_KEY")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Flask Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("FLASKMAIL_MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("FLASKMAIL_MAIL_PASSWORD")
