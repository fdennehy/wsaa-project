# Import required modules from flask
from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS, cross_origin
import random # to randomly generate health scores and account ids

# Import required DAO modules
from accountDAO import accountDAOInstance
from contactDAO import contactDAOInstance

# Import requests to call Random Usert API
import requests

app = Flask(__name__, static_url_path='', static_folder='static') # serve static files from static/, but make them accessible at the root URL.
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

# Serve html file to root url /
@app.route('/')
@cross_origin()
def dashboard():
    return render_template("dashboard.html")


### ACCOUNT ROUTING ###


# Route to get all accounts: curl https://fdennehy.pythonanywhere.com/accounts
@app.route('/accounts')
@cross_origin()
def getAllAccounts():
    results = accountDAOInstance.getAllAccounts()
    return jsonify(results)

# Route to get an account by id: curl https://fdennehy.pythonanywhere.com/accounts/id"
@app.route('/accounts/<int:id>')
@cross_origin()
def getAccountById(id):
    account = accountDAOInstance.findAccountByID(id)
    if account:
        return jsonify(account)
    else:
        return jsonify({"error": "Account not found"}), 404

# Route to create new account: 
# curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Server Test Corp", "website": "http://servertest.com", "revenue": "0", "region":"Africa"}' https://fdennehy.pythonanywhere.com/accounts
@app.route('/accounts', methods=['POST'])
@cross_origin()
def createAccount():
    account = request.get_json()
    if not account:
        abort(400, description="Invalid Input")
    new_account = accountDAOInstance.createAccount(account)
    if new_account:
        return jsonify(new_account), 201
    else:
        return jsonify({"error": "Account creation failed"}), 500

# Route to update account by ID
# curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "Updated Server Corp", "website": "http://updatedserver.com", "revenue": "0", "region":"Antarctica"}' https://fdennehy.pythonanywhere.com/accounts/id
@app.route('/accounts/<int:id>', methods=['PUT'])
@cross_origin()
def updateAccount(id):
    account = request.get_json()
    if not account:
        abort(400, description="Invalid input")
    updated = accountDAOInstance.updateAccount(id, account)
    if updated:
        return jsonify(updated)
    else:
        return jsonify({'error': 'Account update failed'}), 500
        
# Route to delete an account by id: curl -X DELETE https://fdennehy.pythonanywhere.com/accounts/id
@app.route('/accounts/<int:id>' , methods=['DELETE'])
@cross_origin()
def deleteAccount(id):
    result = accountDAOInstance.deleteAccount(id)
    if result:
        return jsonify({"success":True, "message":"Account deleted successfully"}),200
    else:
        return jsonify({"error":"Account deletion failed"}), 404

# Route to delete all account data: curl -X DELETE https://fdennehy.pythonanywhere.com/accounts/wipe
@app.route('/accounts/wipe', methods=['DELETE'])
@cross_origin()
def wipeAllAccounts():
    result = accountDAOInstance.deleteAllAccounts()
    if result:
        return jsonify({"success":True, "message":"All accounts deleted successfully."}), 200
    else:
        return jsonify({"error":"Failed to delete accounts or no accounts found"}), 500

# Route to generate dummy account data: curl -X POST https://fdennehy.pythonanywhere.com/accounts/dummy
@app.route('/accounts/dummy', methods=['POST'])
@cross_origin()
def insertDummyAccounts():
    result = accountDAOInstance.dummyAccountDataInsert()
    if result:
        return jsonify({"success": True, "message": "Dummy account data inserted successfully.", "accounts": result}), 201
    else:
        return jsonify({"error": "Failed to insert dummy account data."}), 500

# Route to 
@app.route('/accounts/insights', methods=['GET'])
def avg_health_score_per_account():
    result = accountDAOInstance.avgAccountHealthScore()
    return jsonify(result)

### CONTACT ROUTING ###


# Route to get all contacts: curl https://fdennehy.pythonanywhere.com/contacts
@app.route('/contacts')
@cross_origin()
def getAllContacts():
    results = contactDAOInstance.getAllContacts()
    return jsonify(results)

# Route to get a contact by id: curl https://fdennehy.pythonanywhere.com/contacts/id"
@app.route('/contacts/<int:id>')
@cross_origin()
def getContactById(id):
    contact = contactDAOInstance.findContactByID(id)
    if contact:
        return jsonify(contact)
    else:
        return jsonify({"error": "Contact not found"}), 404

# Route to create a new contact: 
@app.route('/contacts', methods=['POST'])
@cross_origin()
def createContact():
    contact = request.get_json()
    if not contact:
        abort(400, description="Invalid Input")
    new_contact = contactDAOInstance.createContact(contact)
    if new_contact:
        return jsonify(new_contact), 201
    else:
        return jsonify({"error": "Contact creation failed"}), 500

# Route to update contact by ID
@app.route('/contacts/<int:id>', methods=['PUT'])
@cross_origin()
def updateContact(id):
    contact = request.get_json()
    if not contact:
        abort(400, description="Invalid input")
    updated = contactDAOInstance.updateContact(id, contact)
    if updated:
        return jsonify(updated)
    else:
        return jsonify({'error': 'Contact update failed'}), 500
        
# Route to delete a contact by id: curl -X DELETE https://fdennehy.pythonanywhere.com/contacts/id
@app.route('/contacts/<int:id>' , methods=['DELETE'])
@cross_origin()
def deleteContact(id):
    result = contactDAOInstance.deleteContact(id)
    if result:
        return jsonify({"success":True, "message":"Contact deleted successfully"}),200
    else:
        return jsonify({"error":"Contact deletion failed"}), 404

# Route to generate and insert a random contact: curl -X POST https://fdennehy.pythonanywhere.com/contacts/dummy
@app.route('/contacts/dummy', methods=['POST'])
@cross_origin()
def insertDummyContact():
    try:
        # no. of users to be created
        count = min(int(request.args.get("count", 1)), 100)  # default 1, max 100
        inserted_contacts = []

        # Get available account IDs
        accounts = accountDAOInstance.getAllAccounts()
        account_ids = [a["id"] for a in accounts]
        if not account_ids:
            return jsonify({"error": "No account found. Cannot assign contact."}), 400

        for _ in range(count):
            # Fetch dummy user from randomuser api
            response = requests.get("https://randomuser.me/api/")
            response.raise_for_status()
            user = response.json()["results"][0]

            # Build dummy contact, assiging a random account ID from those available and generate a random health score.
            dummy_contact = {
                "account_id": random.choice(account_ids),
                "first_name": user["name"]["first"],
                "last_name": user["name"]["last"],
                "email": user["email"],
                "phone": user["phone"],
                "health_score": random.randint(1, 100)
            }

            result = contactDAOInstance.dummyContactDataInsert(dummy_contact)
            if result:
                inserted_contacts.append(dummy_contact)

        return jsonify({
            "success": True,
            "message": f"{len(inserted_contacts)} dummy contacts inserted.",
            "contacts": inserted_contacts
        }), 201

    except Exception as e:
        print(f"Error in insertDummyContact: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__' :
    app.run(debug= True)