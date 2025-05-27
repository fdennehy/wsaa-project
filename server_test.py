# Script to test flask app server functions

import requests

# BASE URLs
ACCOUNT_URL = "https://fdennehy.pythonanywhere.com/accounts"
CONTACT_URL = "https://fdennehy.pythonanywhere.com/contacts"


print("\n ACCOUNT TESTS \n")


# 1.1 Get all accounts: curl https://fdennehy.pythonanywhere.com/accounts
print("\n GET all accounts: \n")
response = requests.get(ACCOUNT_URL)
print(response.json())

# 1.2 Create new account
# curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Server Test Corp", "website": "http://servertest.com", "revenue": "0", "region":"Africa"}' https://fdennehy.pythonanywhere.com/accounts
print("\n Create new account (POST): \n")
new_account = {
    "name": "Server Test Corp", 
    "website": "http://servertest.com", 
    "revenue":"0", 
    "region":"Africa"
}
response = requests.post(ACCOUNT_URL, json=new_account)
created = response.json()
print("\n Created account: \n", created)

new_id = created.get("id") 
if not new_id:
    print("\n Failed to create account. Exiting test. \n")
    exit(1)

# 1.3 Get an account by id: curl https://fdennehy.pythonanywhere.com/accounts/{new_id}"
print(f"\n GET account by ID {new_id}: \n")
response = requests.get(f"{ACCOUNT_URL}/{new_id}")
print(response.json())

# 1.4 Update account
# curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "Updated Server Corp", "website": "http://updatedserver.com", "revenue": "0", "region":"Antarctica"}' https://fdennehy.pythonanywhere.com/accounts/id
print(f"\n Update account (PUT) with ID {new_id}:")
updated_data = {
    "name": "Updated Server Corp", 
    "website": "http://updatedserver.com", 
    "revenue":"0", 
    "region":"Antarctica"
}
response = requests.put(f"{ACCOUNT_URL}/{new_id}", json=updated_data)
print("\n Status code:", response.status_code) # debug
print("\n Response content:", repr(response.text)) # debug

if response.status_code in (200, 201):
    print(response.json())
else:
    print("\n Update failed, no JSON returned")

# 1.5 Delete an account by id: curl -X DELETE https://fdennehy.pythonanywhere.com/accounts/{new_id}
print(f"\n DELETE account {new_id}: \n")
response = requests.delete(f"{ACCOUNT_URL}/{new_id}")
print(response.json())

# 1.6 Verify deletion: curl -i https://fdennehy.pythonanywhere.com/accounts/{new_id}
print(f"\n GET deleted account {new_id}: \n")
response = requests.get(f"{ACCOUNT_URL}/{new_id}")
print("Expected 404 or error message:", response.text)

# 1.7 Insert dummy accounts: curl -X DELETE curl -X POST https://fdennehy.pythonanywhere.com/accounts/dummy
print("\n Rehydrating database with dummy data: \n")
response = requests.post(f"{ACCOUNT_URL}/dummy")
if response.status_code == 201:
    dummy_data = response.json()
    print("Dummy insert success:", dummy_data.get("message"))
else:
    print("Dummy data insert failed:", response.text)

# 1.8 Verify dummy account have been created: curl https://fdennehy.pythonanywhere.com/accounts
print("\n Confirming dummy accounts have been created: \n")
response = requests.get(ACCOUNT_URL)
print(response.json())


print("\n CONTACT TESTS \n")


# 2.1 Get all contacts
print("\n GET all contacts: \n")
response = requests.get(CONTACT_URL)
print("Status Code:", response.status_code) # debug
print("Raw Response:", response.text) # debug

if response.status_code == 200:
    print("JSON Response:", response.json())
else:
    print("Failed to retrieve contacts.")

# 2.2 Create a new contact
print("\n Create new contact (POST): \n")

# Get current accounts to find a valid account_id
response = requests.get(ACCOUNT_URL)
accounts = response.json()
if not accounts:
    print("No accounts available. Cannot create contact.")
    exit(1)

account_id = accounts[0]["id"]  # Get ID of the first account

new_contact = {
    "account_id": account_id,
    "first_name": "Test",
    "last_name": "Contact",
    "email": "test.contact@example.com",
    "phone": "123-456-7890",
    "health_score": 85
}
response = requests.post(CONTACT_URL, json=new_contact)
created_contact = response.json()
print("\n Created contact: \n", created_contact)

contact_id = created_contact.get("id")
if not contact_id:
    print("\n Failed to create contact. Skipping contact-specific tests.\n")
    exit(1)  # Stop test if creation fails

# 2.3 Get contact by ID
print(f"\n GET contact by ID {contact_id}: \n")
response = requests.get(f"{CONTACT_URL}/{contact_id}")
print(response.json())

# 2.4 Update contact
print(f"\n Update contact (PUT) with ID {contact_id}:")
updated_contact = {
    "account_id": account_id,  # Reuse valid account_id
    "first_name": "Updated",
    "last_name": "Contact",
    "email": "updated.contact@example.com",
    "phone": "987-654-3210",
    "health_score": 90
}
response = requests.put(f"{CONTACT_URL}/{contact_id}", json=updated_contact)
print("\n Update response:", response.json())

# 2.5 Delete contact
print(f"\n DELETE contact {contact_id}: \n")
response = requests.delete(f"{CONTACT_URL}/{contact_id}")
print(response.json())

# 2.6 Confirm contact deletion
print(f"\n GET deleted contact {contact_id}: \n")
response = requests.get(f"{CONTACT_URL}/{contact_id}")
print("Expected 404 or error message:", response.text)

# 2.7. Insert dummy contacts
print("\n Inserting dummy contacts: \n")
response = requests.post(f"{CONTACT_URL}/dummy", params={"count": 2})
if response.status_code == 201:
    dummy_contacts = response.json()
    print("Dummy contacts inserted:", dummy_contacts.get("message"))
else:
    print("Dummy contact insert failed:", response.text)

# 2.8. Confirm dummy contact creation
print("\n Confirming dummy contacts have been created: \n")
response = requests.get(CONTACT_URL)
print(response.json())