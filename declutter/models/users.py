import pytz
import jwt
from typing import Type
from dateutil import tz
from datetime import datetime, timedelta, tzinfo 
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedSerializer

# App imports
from declutter.utilities.backend import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(200), nullable = False, unique = True)
    user_username = db.Column(db.String(40), nullable = False, unique = True)
    user_password = db.Column(db.String(40), nullable = False)
    user_date_created_utc = db.Column(db.DateTime, nullable = False, default = datetime.now(pytz.UTC))
    posts = db.relationship('Posts', backref = 'post_author', lazy = True)


    def get_reset_token(self, expires_sec: int = 600):
        reset_token = jwt.encode(
            key = current_app.config.get('SECRET_KEY'), algorithm = 'HS256',
            payload = {'user_id': self.user_id, 'exp': datetime.now(pytz.UTC) + timedelta(seconds = expires_sec)}, )

        return reset_token


    @staticmethod
    def verify_reset_token(reset_token):
        try:
            payload = jwt.decode(key = current_app.config.get('SECRET_KEY'), algorithms = 'HS256', jwt = reset_token, )
        except:
            return None

        return Users.query.get(payload.get('user_id'))


    def get_id(self):
        return self.user_id


    def __repr__(self):
        return f"User('{self.user_id}', {self.user_email}', '{self.user_username}', '{self.user_date_created_utc}')"