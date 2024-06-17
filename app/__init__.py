from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__,static_url_path='/static', static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)

from . import models

# Import routes
from app import routes