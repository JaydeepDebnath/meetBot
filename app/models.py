from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from app import app

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    contactNumber = db.Column(db.String(15),nullable=False)


class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_link = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    owner = db.relationship('User', backref='bots')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)