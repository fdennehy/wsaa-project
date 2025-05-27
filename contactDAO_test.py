# Script to test the various functions in the contactDAO

from contactDAO import contactDAO

dao = contactDAO() # create an instance

# GET all contacts
print("\n GET all contacts: \n")
print(dao.getAllContacts())

# CREATE a new contact
print("Creating a new contact 'DAO Tester': \n")
new_contact = dao.createContact ({
    "first_name": "DAO",
    "last_name": "Tester",
    "email": "dao.tester@example.com",
    "phone": "555-0100",
    "health_score": 75,
    "account_id": 3  # Make sure this account ID exists in your DB
})
new_contact_id = new_contact['id']
print(f"Created contact {new_contact} \n")

# GET new contact by ID
print("\n Testing find contact by ID function: \n")
print(dao.findContactByID(new_contact_id))

# UPDATE the contact
print(f"\nTesting update contact function on contact with ID {new_contact_id} \n")
updated_contact = dao.updateContact(new_contact_id, {
    "first_name": "UpdatedDAO",
    "last_name": "Tester",
    "email": "updated.dao@example.com",
    "phone": "555-0200",
    "health_score": 85,
    "account_id": 3
})
print(f"\n Updated account {updated_contact} with ID: {new_contact_id} \n")

# DELETE the contact
print(f"DELETE contact with ID {new_contact_id}:")
dao.deleteContact(new_contact_id)
assert dao.findContactByID(new_contact_id) is None, "Deletion failed"

# Confirm recent addition has been deleted
print("\nContact deleted. Veryifying deletion: \n")
print(dao.getAllContacts())