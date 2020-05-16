from application import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    user_id = db.Column(db.String(255), nullable=False, unique=True, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), unique=False)
    last_name = db.Column(db.String(255), unique=False)
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    # user_type is either "SME" or "Startup" or None
    user_type = db.Column(db.String(60))
    industry = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    client_encodedkey = db.Column(db.String(255))

    # one-to-many relationship
    grants = db.relationship('Grant', backref='user', lazy=True)

    # one-to-many relationship
    projects = db.relationship('Project', backref='user', lazy=True)

    # one-to-many relationship
    current_accounts = db.relationship('CurrentsAccount', backref='user', lazy=True)

    # one-to-many relationship
    loan_accounts = db.relationship('LoanAccount', backref='user', lazy=True)

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
    grant_amount = db.Column(db.Float(11,2))
    grant_type = db.Column(db.String(255))
    
    #user foreign key
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    project_name = db.Column(db.String(255), unique=False)
    project_goal = db.Column(db.Float(11,2))
    project_description = db.Column(db.Text(100000), unique=False)

    #user foreign key
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)

    #one to many relationship
    investments = db.relationship('Investment', backref='project', lazy=True)

class CurrentsAccount(db.Model):
    #encoded key
    currentacc_key = db.Column(db.String(255), primary_key=True, nullable=False, unique=True)
    interest_rate = db.Column(db.Float(8,4))
    
    #user foreign key
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)

class LoanAccount(db.Model):
    #encoded key
    loanacc_key = db.Column(db.String(255), primary_key=True, nullable=False, unique=True)
    interest_rate = db.Column(db.Float(8,4))
    loan_amount = db.Column(db.Float(11,2))
    arrears_tolerance_period = db.Column(db.Integer)
    grace_period = db.Column(db.Integer)
    repayment_installments = db.Column(db.Float(9,2))
    repayment_period_count = db.Column(db.Integer)
    periodic_payment = db.Column(db.Integer)
    repayment_period_unit = db.Column(db.Integer)
    customfield_id = db.Column(db.String(255))
    value = db.Column(db.String(255))

    #user foreign key
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)

class Investment(db.Model):
    investment_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    investment_amount = db.Column(db.Float(9,2))

    #user foreign key
    user_id = db.Column(db.String(255), db.ForeignKey('user.user_id'), nullable=False)

    #project foreign key
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)

