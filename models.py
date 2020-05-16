from application import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), unique=False)
    last_name = db.Column(db.String(255), unique=False)
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)

    # one-to-many relationship
    grants = db.relationship('Grant', backref='user', lazy=True)

    # one-to-many relationship
    project = db.relationship('Project', backref='user', lazy=True)

    def get_id(self):
        return (self.user_id)

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
    
    def is_active(self):
        """True, as all users are active."""
        return True
    
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Grant(db.Model):
    grant_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    grant_name = db.Column(db.String(255), unique=False)
    grant_amount = db.Column(db.Float)
    user_name = db.Column(db.String(255), db.ForeignKey('user.user_name'), nullable=False)
    grant_type = db.Column(db.String(255))

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    project_name = db.Column(db.String(255), unique=False)
    project_goal = db.Column(db.Float)
    project_description = db.Column(db.String(100000), unique=False)
    user_name = db.Column(db.String(255), db.ForeignKey('user.user_name'), nullable=False)
