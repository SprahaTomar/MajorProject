
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False, default='farmer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Users {}>'.format(self.username)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    investment_goal = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    current_investment = db.Column(db.Float, nullable=False, default=0)
    
    # Define the foreign key relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('projects', lazy=True))

    def __init__(self, project_name, description, investment_goal, location, user_id):
        self.project_name = project_name
        self.description = description
        self.investment_goal = investment_goal
        self.location = location
        self.user_id = user_id

    def __repr__(self):
        return f"<Project {self.project_name}>"


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    amount = db.Column(db.Float)
    investment_date = db.Column(db.DateTime)
    roi = db.Column(db.Float)

    def __repr__(self):
        return '<Investment {}>'.format(self.id)



