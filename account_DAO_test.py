# Script to test the various functions in the DAO

from account_DAO import accountDAO

dao = accountDAO() # create an instance

# Get all accounts
print("\nTesting all account functions:")
print(dao.getAllAccounts())

# Create a new account
print("\nTesting account creation function:")
new_account = dao.createAccount({"account_name": "Test Corp", "website": "testcorp.com"})
new_id = new_account['account_id']
print(f"Created account {new_account}")

# Find by ID
print("\nTesting find account by ID function:")
print(dao.findAccountByID(new_id))

# Update the account
print(f"\nTesting update account function on account with ID {new_id}")
updated_account = dao.updateAccount(new_id, {"account_name": "Updated Corp", "website": "updatedcorp.com"})
print(f"Updated account {updated_account} with ID: {new_id}")

# Delete the account
print("\nTesting account deletion by ID function:")
dao.deleteAccount(new_id)

# FInal check
print("\nFinal account list:")
print(dao.getAllAccounts())