import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='static',
)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)

from declutter import routes