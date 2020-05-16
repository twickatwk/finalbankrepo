from flask import redirect, url_for, render_template, request, flash, session,jsonify
from application import application
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Optional, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json
from models import User, Grant, Project, CurrentsAccount, LoanAccount, Investment
from application import db
import requests
import random

def validate_password_length(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError("Password needs to be at least 8 characters long")

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    user_name = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8)])
    nric = StringField('NRIC', validators=[InputRequired(), Length(min=9)])


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

        # ==========  Mambu  ======================
        try:
            firstName = registration_form.first_name.data
            lastName = registration_form.last_name.data
            preferredLanguage = "ENGLISH"
            notes = ""
            assignedBranchKey = "8a8e878e71c7a4d70171ca644def1259"
            basicInfo = {"firstName": firstName, "lastName": lastName, "preferredLanguage": preferredLanguage, "notes": notes, "assignedBranchKey": assignedBranchKey}
            identificationDocumentTemplateKey = "8a8e867271bd280c0171bf7e4ec71b01"
            issuingAuthority = "Immigration Authority of Singapore"
            documentType = "NRIC"
            validUntil = "2200-01-01"
            documentId = registration_form.nric.data
            identity = [{"identificationDocumentTemplateKey":identificationDocumentTemplateKey, "issuingAuthority":issuingAuthority, "documentType":documentType, "validUntil":validUntil, "documentId":documentId}]
            createClientJson = json.dumps({"client":basicInfo, "idDocuments":identity})
            headers = {'content-type': 'application/json'}
            response = requests.post("https://razerhackathon.sandbox.mambu.com/api/clients", data=createClientJson, headers=headers, auth=('Team66', 'passEE8295411'))
            response_data = response.json()
            user_encoded_id = response_data["client"]["encodedKey"]
        except Exception as e:
            flash('Something went wrong. Please try again.')
            return redirect(url_for('index'))
        # =====================================================================================

        new_user = User(user_name=registration_form.user_name.data,
                        password=generate_password_hash(registration_form.password.data,
                                                        method='pbkdf2:sha256'),
                        first_name=registration_form.first_name.data,
                        last_name=registration_form.last_name.data,
                        user_id = user_encoded_id)

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

# API endpoint for react to obtain all Projects by the Logged in User
@application.route("/getProjectsByUser")
def getProjectsByUser():
    # SQL Alchemy Code to retrieve all data from the db
    results = Project.query.filter_by(user_id=current_user.user_id)
    data_set = {}
    # Loop through the results array and add it into the dictionary of Project objects
    for record in results:
        data_set[record.project_id] = [record.project_name, record.project_description, str(record.project_goal)]

    # Convert dataset into JSON object and return it to the fetch command
    return jsonify(data_set)

@application.route('/grants')
def grant_page():
    currUserFirstName = current_user.first_name
    currUserLastName = current_user.last_name
    currUserID = current_user.user_id
    #grant = Grant.query.filter_by(user_id=currUserID)
    
    all_loans = LoanAccount.query.filter_by(user_id=currUserID).all()
    #for i in all_loans:
    #    print(i.interest_rate)
    
    return render_template('grants.html', fname = currUserFirstName, lname = currUserLastName,  all_loans = all_loans)

@application.route('/loans')
#@login_required
def loan_page():
    return render_template('loans.html')

@application.route('/loans_processing', methods = ['POST', 'GET'])
#@login_required
def loanprocessing_page():
    if request.method == 'POST':
        result = request.form
        currUserID = current_user.user_id
        print(CurrentsAccount.query.filter_by(user_id = currUserID).first() == None)
        if(CurrentsAccount.query.filter_by(user_id = currUserID).first() == None):
            #if client do not have Current Account
            curracct_name = "Digital Account"
            accountHolderType = "CLIENT"
            accountHolderKey = currUserID
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
            response_data = response.json()
            savingsaccount_encoded_id = response_data["savingsAccount"]["encodedKey"]

            new_currentacct = CurrentsAccount(currentacc_key=savingsaccount_encoded_id,
                        interest_rate = 0.05,
                        user_id = currUserID)

            db.session.add(new_currentacct)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash('Something went wrong. Please try again.')
                return redirect(url_for('grant_page'))

        #Create new loan
        accountHolderType = "CLIENT"
        accountHolderKey = currUserID
        productTypeKey = "8a8e867271bd280c0171bf768cc31a89"
        assignedBranchKey = "8a8e878e71c7a4d70171ca644def1259"
        loanName = result["loanName"]
        loanAmount = float(result["loanAmount"])
        interestRate = "2"
        arrearsTolerancePeriod = "0"
        gracePeriod = "0"
        repaymentInstallments = "10"
        repaymentPeriodCount = "1"
        periodicPayment = 0
        repaymentPeriodUnit = result["repayment_period_unit"]
        value = current_user.first_name + current_user.last_name + str(random.randint(1,88888))
        customFieldID = "IDENTIFIER_TRANSACTION_CHANNEL_I"
        disbursementDetails = {"customInformation":[{"value":value, "customFieldID":customFieldID}]}
        loanAccountJson = {"accountHolderType":accountHolderType, "accountHolderKey":accountHolderKey, "productTypeKey":productTypeKey, "assignedBranchKey":assignedBranchKey, "loanName":loanName, "loanAmount":loanAmount, "interestRate":interestRate, "arrearsTolerancePeriod":arrearsTolerancePeriod, "gracePeriod":gracePeriod, "repaymentInstallments":repaymentInstallments, "repaymentPeriodCount":repaymentPeriodCount,"periodicPayment":periodicPayment, "repaymentPeriodUnit":repaymentPeriodUnit, "disbursementDetails":disbursementDetails}
        createLoanAccountJson = json.dumps({"loanAccount":loanAccountJson})
        print(createLoanAccountJson)
        headers = {'content-type': 'application/json'}
        response = requests.post("https://razerhackathon.sandbox.mambu.com/api/loans", data=createLoanAccountJson, headers=headers, auth=('Team66', 'passEE8295411'))
        response_data = response.json()
        print(response_data)
        loansaccount_encoded_id = response_data["loanAccount"]["encodedKey"]

        new_Loans = LoanAccount(loanacc_key=loansaccount_encoded_id,
                        interest_rate=interestRate,
                        loan_amount=loanAmount,
                        arrears_tolerance_period = arrearsTolerancePeriod,
                        grace_period = int(gracePeriod),
                        repayment_installments = float(repaymentInstallments),
                        repayment_period_count = int(repaymentPeriodCount),
                        periodic_payment = periodicPayment,
                        repayment_period_unit = repaymentPeriodUnit,
                        customfield_id = customFieldID,
                        value = value,
                        user_id = currUserID)

        db.session.add(new_Loans)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Something went wrong. Please try again.')
            return redirect(url_for('grant_page'))

        flash('You have successfully applied for a loan.')
        return redirect(url_for('grant_page'))
    else:
        return redirect(url_for('grant_page'))


# @application.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404


# This code might not be needed
@application.route('/crowdsourcing')
def crowdsourcing():
    return render_template('crowdsourcing.html')

# End Point to render crowdsourcing web page back to the user
@application.route('/investors')
def investors_page():
    return render_template('investors.html')

# API endpoint for react to obtain all Projects
@application.route("/getProjects")
def getProjects():
    # SQL Alchemy Code to retrieve all data from the db
    results = Project.query.all()
    data_set = {}
    # Loop through the results array and add it into the dictionary of Project objects
    for record in results:
        data_set[record.project_id] = [record.project_name, record.project_description, str(record.project_goal)]

    # Convert dataset into JSON object and return it to the fetch command
    return jsonify(data_set)

@application.route("/addFunds")
def addFunds():
    amount = request.args.get('amount')
    project_id = request.args.get('pid')
    new_investment = Investment(investment_amount=amount, user_id=current_user.user_id, project_id=project_id)

    db.session.add(new_investment)

    #TODO: Retrieve all investments for that particular project
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Something went wrong. Please try again.')
        return ""

    return ""



@application.route('/cs_processing', methods = ['POST', 'GET'])
#@login_required
def csprocessing_page():
    if request.method == 'POST':
        result = request.form
        currUserID = current_user.user_id

        #Create new loan
        project_name = result["projectName"]
        project_goal = result["fundingGoals"]
        project_description = result["list_info"]
        new_Project = Project(project_name=project_name,
                        project_goal=project_goal,
                        project_description=project_description,
                        user_id = currUserID)
        db.session.add(new_Project)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Something went wrong. Please try again.')
            return redirect(url_for('grant_page'))

        flash('You have successfully added your project.')
        return redirect(url_for('grant_page'))
    else:
        return redirect(url_for('grant_page'))
