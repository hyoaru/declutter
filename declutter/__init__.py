from typing import Type
from datetime import datetime
from flask import request
from flask import Flask
from flask_admin.contrib.sqla import ModelView

# App imports
from declutter.utilities.backend import db, bcrypt, login_manager, mail, migrate
from declutter.config import Config
from declutter.utilities.datetime import datetime_tolocal
from declutter.utilities.sidebar_elements import get_posts_recent_n, get_users_recent_n, get_daily_random_quotes


# Blueprints
from declutter.blueprints.main.views import main as blueprint_main
from declutter.blueprints.posts.views import posts as blueprint_posts
from declutter.blueprints.authentication.views import authentication as blueprint_authentication
from declutter.blueprints.users.general.views import users_general as blueprint_users_general
from declutter.blueprints.users.account.views import users_account as blueprint_users_account
from declutter.blueprints.errors.handlers import errors as blueprint_errors

# Database models
from declutter.models.users import Users
from declutter.models.posts import Posts

def create_app(config_class: Type[Config] = Config) -> Flask:
    app = Flask(__name__, template_folder = 'templates', static_folder = 'static')
    app.config.from_object(config_class)
    
    # Blueprint registration
    app.register_blueprint(blueprint_main)
    app.register_blueprint(blueprint_posts)
    app.register_blueprint(blueprint_authentication)
    app.register_blueprint(blueprint_users_general)
    app.register_blueprint(blueprint_users_account)
    app.register_blueprint(blueprint_errors)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'authentication.login'
    login_manager.login_message_category = 'warning'

    with app.app_context():
        db.create_all()
        print(f'\nCreated table names: {db.engine.table_names()}')

    @app.context_processor
    def inject_global_elements():
        return dict(
            datetime_tolocal = datetime_tolocal, datetime_utcnow = datetime.utcnow(), 
            posts_recent_n = get_posts_recent_n(5), users_recent_n = get_users_recent_n(5), 
            quote_of_the_day = get_daily_random_quotes(), request = request)

    return app
