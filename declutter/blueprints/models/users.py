from datetime import datetime
from declutter.database import db

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(200), nullable = False, unique = True)
    user_username = db.Column(db.String(40), nullable = False, unique = True)
    user_password = db.Column(db.String(40), nullable = False)
    user_date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    posts = db.relationship('Posts', backref = 'post_author', lazy = True)

    def __repr__(self):
        return f"User('{self.user_username}', '{self.user_email}'"