from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

# Import database models
from declutter.blueprints.models.users import Users
from declutter.blueprints.models.posts import Posts