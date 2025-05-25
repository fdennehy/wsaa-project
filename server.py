from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from account_DAO import accountDAOInstance

app = Flask(__name__, static_url_path='', static_folder='.')
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return "Account API Running!"

# Get all accounts: curl "http://127.0.0.1:5000/accounts"
@app.route('/accounts')
@cross_origin()
def getAllAccounts():
    results = accountDAOInstance.getAllAccounts()
    return jsonify(results)

# Get an account by id: curl "http://127.0.0.1:5000/accounts/2"
@app.route('/accounts/<int:id>')
@cross_origin()
def findById(id):
    found_account = accountDAOInstance.findAccountByID(id)
    if not found_account:
        abort(404)
    return jsonify(found_account)

# Create new account: curl  -i -H "Content-Type:application/json" -X POST -d "{\"account_name\":\"webservicesinc\",\"website\":\"webservicesinc.com\"}" http://127.0.0.1:5000/accounts
@app.route('/accounts', methods=['POST'])
@cross_origin()
def createAccount():
    if not request.json:
        abort(400)
    # basic validation: require at least account_name, website can be optional
    if 'account_name' not in request.json:
        abort(400) 
    account = {
        "account_name": request.json['account_name'],
        "website": request.json.get('website', "") # use get() for optional key
    }
    added_account = accountDAOInstance.createAccount(account)
    
    return jsonify(added_account), 201

# Update an existing account: curl  -i -H "Content-Type:application/json" -X PUT -d ""{\"account_name\":\"webservicesinc\",\"website\":\"webservicesinc.com\"}" http://127.0.0.1:5000/accounts/2
@app.route('/accounts/<int:id>', methods=['PUT'])
@cross_origin()
def update(id):
    found_account = accountDAOInstance.findAccountByID(id)
    if not found_account:
        abort(404)
    if not request.json:
        abort(400)

    reqJson = request.json
    if 'account_name' in reqJson and type(reqJson['account_name']) is not str:
        abort(400)
    if 'website' in reqJson and type(reqJson['website']) is not str:
        abort(400)

    if 'account_name' in reqJson:
        found_account['account_name'] = reqJson['account_name']
    if 'website' in reqJson:
        found_account['website'] = reqJson['website']

    accountDAOInstance.updateAccount(id,found_account)
    return jsonify(found_account)
        
# Delete an account by id
@app.route('/accounts/<int:id>' , methods=['DELETE'])
@cross_origin()
def deleteAccount(id):
    accountDAOInstance.deleteAccount(id)
    return jsonify({"done":True})

if __name__ == '__main__' :
    app.run(debug= True)