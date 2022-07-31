from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Import database models
from declutter.blueprints.models.users import Users
from declutter.blueprints.models.posts import Posts