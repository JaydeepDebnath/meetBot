from flask import Flask

app = Flask(__name__)

# Load configuration settings
app.config.from_object('config')

# Import routes
from app import routes