from flask import redirect, url_for, render_template, request, flash, session
from application import application
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json
from models import User, Grant
from application import db


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    user_name = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8)])
    

class LoginForm(FlaskForm):
    user_login = StringField('username or email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

@application.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    registration_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('index.html', registration_form=registration_form, login_form=login_form)

@application.route('/register', methods = ['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    login_form = LoginForm()

    if registration_form.validate_on_submit():
        #check whether user's 2 keyed passwords are the same
        pw1 = registration_form.password.data
        pw2 = registration_form.password2.data
        
        if pw1 != pw2:
            flash('Your passwords do not match. Please try again.')
            return redirect(url_for('register'))
        
        # ========== IMPORTANT: Wrong way to add id! Should use Mambu id ======================
        # ========== This is just a workaround to allow site to keep adding new users =========
        id_to_add = 0
        try:
            id_to_add = User.query.order_by(User.user_id.desc()).first().user_id + 1
        except AttributeError:
            id_to_add = 1
        # =====================================================================================

        new_user = User(user_name=registration_form.user_name.data,
                        password=generate_password_hash(registration_form.password.data,
                                                        method='pbkdf2:sha256'),
                        first_name=registration_form.first_name.data,
                        last_name=registration_form.last_name.data,
                        user_id = id_to_add)

        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Something went wrong. Please try again.')
            return redirect(url_for('register'))

        flash('You have successfully registered your account. Please login again to confirm.')

    return render_template("index.html",  registration_form=registration_form, login_form=login_form)


@application.route('/login', methods = ['GET', 'POST'])
def login(): 
    registration_form = RegistrationForm()
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_login = login_form.user_login.data
        user=User.query.filter_by(user_name=user_login).first()

        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user)
            session.permanent = True
            return redirect(url_for('home'))

    return render_template("index.html",  registration_form=registration_form, login_form=login_form)

@application.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html")


@application.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        
    return redirect(url_for('index'))


@application.route('/grants')
def grant_page():
    return render_template('grants.html')

@application.route('/loans')
def loan_page():
    return render_template('loans.html')

@application.route('/loans_processing', methods = ['POST', 'GET'])
def loanprocessing_page():
    if request.method == 'POST':
        result = request.form

        firstName = result["firstName"]
        lastName = result["lastName"]
        preferredLanguage = "ENGLISH"
        notes = result["grant"]
        assignedBranchKey = "8a8e878e71c7a4d70171ca644def1259"
        basicInfo = {"firstName": firstName, "lastName": lastName, "preferredLanguage": preferredLanguage, "notes": notes, "assignedBranchKey": assignedBranchKey}

        identificationDocumentTemplateKey = "8a8e867271bd280c0171bf7e4ec71b01"
        issuingAuthority = "Immigration Authority of Singapore"
        documentType = "NRIC/Passport Number"
        validUntil = "2021-09-12"
        documentId = "S9812345A"
        identity = [{"identificationDocumentTemplateKey":identificationDocumentTemplateKey, "issuingAuthority":issuingAuthority, "documentType":documentType, "validUntil":validUntil, "documentId":documentId}]

        createClientJson = json.dumps({"client":basicInfo, "idDocuments":identity})
        print(createClientJson)

        return render_template('loans_processing.html', result = result)
    else:
        return redirect(url_for('loan_page'))

@application.route('/crowdsourcing')
def crowdsourcing():
    return render_template('crowdsourcing.html')


