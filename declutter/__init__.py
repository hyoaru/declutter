import os
from dotenv import load_dotenv
from flask import Flask
from declutter.database import db, bcrypt, login_manager

def create_app():
    load_dotenv()
    app = Flask(
        __name__, 
        template_folder='templates',
        static_folder='static',
    )

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    return app

app = create_app()
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()
    print(f'\nCreated table names: {db.engine.table_names()}')

from declutter import routes