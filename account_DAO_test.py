# Script to test the various functions in the DAO

from account_DAO import accountDAO

dao = accountDAO() # create an instance

# Get all accounts
print("\nRetrieving all account data... \n")
print(dao.getAllAccounts())

# Create a new account
print("\nCreating a new account 'Test Corp'... \n")
new_account = dao.createAccount({
    "name": "Test Corp", 
    "website": "testcorp.com", 
    "revenue": "0", 
    "region": "Africa"
})
new_id = new_account['id']
print(f"\n Created account {new_account} \n")

# Find by ID
print("\nTesting find account by ID function: \n")
print(dao.findAccountByID(new_id))

# Update the account
print(f"\nTesting update account function on account with ID {new_id} \n")
updated_account = dao.updateAccount(new_id, {
    "name": "Updated Corp", 
    "website": "updatedcorp.com", 
    "revenue": "3000", 
    "region": "Antarctica"
})
print(f"\n Updated account {updated_account} with ID: {new_id} \n")

# Delete the account
print(f"\n Deleting account with id {new_id} \n")
dao.deleteAccount(new_id)
assert dao.findAccountByID(new_id) is None, "Deletion failed"

# Confirm recent addition has been deleted
print("\nAccount deleted. Veryifying deletion: \n")
print(dao.getAllAccounts())

# Delete all accounts
print("\n Deleting all account data: \n")
dao.deleteAllAccounts()

# Confirm database is empty
print("\n All accounts deleted. Checking database is empty... \n")
print(dao.getAllAccounts())

# Re-hydrate the database
print("\n Inserting dummy account data: \n")
dao.dummyDataInsert()
print(dao.getAllAccounts())