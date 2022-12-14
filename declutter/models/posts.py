import pytz
from datetime import datetime, tzinfo
from dateutil import tz

# App imports
from declutter.utilities.backend import db

class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key = True)
    post_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    post_title = db.Column(db.String(100), nullable = False)
    post_content = db.Column(db.Text, nullable = False)
    post_date_created_utc = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    post_isdeleted = db.Column(db.Boolean, nullable = False, default = False)


    def __repr__(self):
        return f"Posts('{self.post_id}', '{self.post_title}', '{self.post_date_created_utc}', '{self.post_author}'"

