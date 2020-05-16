from flask import redirect, url_for, render_template, request, flash, session,jsonify
from application import application
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Optional, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json
from models import User, Grant
from application import db
import requests

def validate_password_length(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError("Password needs to be at least 8 characters long")

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    user_name = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), validate_password_length])
    password2 = PasswordField('Confirm Password', validators=[InputRequired(), validate_password_length])
    

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
            return redirect(url_for('index'))
        
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
            return redirect(url_for('index'))

        flash('You have successfully registered your account. Please login again to confirm.')
        return redirect(url_for('index'))

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
    return render_template('grants.html', )

@application.route('/loans')
#@login_required
def loan_page():
    return render_template('loans.html')

@application.route('/loans_processing', methods = ['POST', 'GET'])
#@login_required
def loanprocessing_page():
    if request.method == 'POST':
        result = request.form

        #If client was not created previously:
        firstName = current_user.first_name
        lastName = current_user.last_name
        preferredLanguage = "ENGLISH"
        notes = result["grant"] #Get from grant DB
        assignedBranchKey = "8a8e878e71c7a4d70171ca644def1259"
        basicInfo = {"firstName": firstName, "lastName": lastName, "preferredLanguage": preferredLanguage, "notes": notes, "assignedBranchKey": assignedBranchKey}
        identificationDocumentTemplateKey = "8a8e867271bd280c0171bf7e4ec71b01"
        issuingAuthority = "Immigration Authority of Singapore"
        documentType = "NRIC/Passport Number"
        validUntil = "2021-09-12"
        documentId = "S9812345A"
        identity = [{"identificationDocumentTemplateKey":identificationDocumentTemplateKey, "issuingAuthority":issuingAuthority, "documentType":documentType, "validUntil":validUntil, "documentId":documentId}]
        createClientJson = json.dumps({"client":basicInfo, "idDocuments":identity})
        headers = {'content-type': 'application/json'}
        response = requests.post("https://razerhackathon.sandbox.mambu.com/api/clients", data=createClientJson, headers=headers, auth=('Team66', 'passEE8295411'))
        print(response.text)

        #if client was already created previously
        #if client do not have Current Account
        curracct_name = "Digital Account"
        accountHolderType = "CLIENT"
        accountHolderKey = "8a8e86fd72174fdd01721b78040f2653" #replace with client encoded key
        accountState = "APPROVED"
        productTypeKey = "8a8e878471bf59cf0171bf6979700440"
        accountType = "CURRENT_ACCOUNT"
        currencyCode = "SGD"
        allowOverdraft = "true" #if has grant == true. else == false
        overdraftLimit = "1000"
        overdraftInterestSettings = {"interestRate":3}
        interestSettings = {"interestRate":"0.05"}
        currentaccount={"name":curracct_name, "accountHolderType":accountHolderType, "accountHolderKey":accountHolderKey, "accountState":accountState, "productTypeKey":productTypeKey, "accountType":accountType, "currencyCode":currencyCode, "allowOverdraft":allowOverdraft, "overdraftLimit":overdraftLimit, "overdraftInterestSettings":overdraftInterestSettings, "interestSettings":interestSettings}
        createCurrentAccountJson = json.dumps({"savingsAccount":currentaccount})
        headers = {'content-type': 'application/json'}
        response = requests.post("https://razerhackathon.sandbox.mambu.com/api/savings", data=createCurrentAccountJson, headers=headers, auth=('Team66', 'passEE8295411'))
        print(response.text)

        #Create new loan
        accountHolderType = "CLIENT"
        accountHolderKey = "8a8e86fd72174fdd01721b78040f2653" #replace with client encoded key
        productTypeKey = "8a8e867271bd280c0171bf768cc31a89"
        assignedBranchKey = "8a8e878e71c7a4d70171ca644def1259"
        loanName = "Student Loan"
        loanAmount = 1000
        interestRate = "2"
        arrearsTolerancePeriod = "0"
        gracePeriod = "0"
        repaymentInstallments = "10"
        repaymentPeriodCount = "1"
        periodicPayment = 0
        repaymentPeriodUnit = "WEEKS"
        value = current_user.first_name + current_user.last_name + "1"
        customFieldID = "IDENTIFIER_TRANSACTION_CHANNEL_I"
        disbursementDetails = {"customInformation":[{"value":value, "customFieldID":customFieldID}]}
        loanAccountJson = {"accountHolderType":accountHolderType, "accountHolderKey":accountHolderKey, "productTypeKey":productTypeKey, "assignedBranchKey":assignedBranchKey, "loanName":loanName, "loanAmount":loanAmount, "interestRate":interestRate, "arrearsTolerancePeriod":arrearsTolerancePeriod, "gracePeriod":gracePeriod, "repaymentInstallments":repaymentInstallments, "repaymentPeriodCount":repaymentPeriodCount,"periodicPayment":periodicPayment, "repaymentPeriodUnit":repaymentPeriodUnit, "disbursementDetails":disbursementDetails}
        createLoanAccountJson = json.dumps({"loanAccount":loanAccountJson})
        headers = {'content-type': 'application/json'}
        response = requests.post("https://razerhackathon.sandbox.mambu.com/api/loans", data=createLoanAccountJson, headers=headers, auth=('Team66', 'passEE8295411'))
        print(response.text)
        return render_template('loans_processing.html', result = result)
    else:
        return redirect(url_for('loan_page'))

@application.route('/crowdsourcing')
def crowdsourcing():
    return render_template('crowdsourcing.html')

@application.route('/investors')
def investors_page():
    
    return render_template('investors.html')

@application.route("/getProjects")
def getProjects():
    # this is the piece to be changed
    data_set = {"SpaceX": ["Falcon Rocket", "Falcon 9 is a partially reusable two-stage-to-orbit medium lift launch vehicle designed and manufactured by SpaceX in the United States. It is powered by Merlin engines, also developed by SpaceX, burning cryogenic liquid oxygen and rocket-grade kerosene as propellants."], "DeepMind": ["AlphaGo", "AlphaGo is a computer program that plays the board game Go."]}
    # Convert dataset into JSON object and return it
    return jsonify(data_set)
