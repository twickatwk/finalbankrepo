from flask import Flask, redirect, url_for, render_template, request
import json

application = Flask(__name__)

@application.route('/')
def home_page():
    return render_template("index.html")

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

@application.route('/index2')
def home_page2():
    return render_template("index2.html")



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()