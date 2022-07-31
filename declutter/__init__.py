import os
from dotenv import load_dotenv
from flask import Flask
from declutter.database import db

def create_app():
    load_dotenv()
    app = Flask(
        __name__, 
        template_folder='templates',
        static_folder='static',
    )
    
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

    return app

app = create_app()
db.init_app(app)

with app.app_context():
    db.create_all()
    print(db.engine.table_names())

from declutter import routes