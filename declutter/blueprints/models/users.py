import pytz
from datetime import datetime, tzinfo
from dateutil import tz
from declutter.database import db, login_manager
from flask_login import UserMixin

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

    def __repr__(self):
        return f"User('{self.user_id}', {self.user_email}', '{self.user_username}', '{self.user_date_created_utc}')"

    def get_id(self):
        return self.user_id