from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Import database models
from declutter.blueprints.models.users import Users
from declutter.blueprints.models.posts import Posts