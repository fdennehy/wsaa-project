from account_DAO import accountDAO

# Get all
print(accountDAO.getAll())

# Create new
new_account = {"account_name": "Test Corp", "website": "testcorp.com"}
new_id = accountDAO.create(new_account)
print("Created ID:", new_id)

# Update
accountDAO.update({"id": new_id, "account_name": "Updated Corp", "website": "updatedcorp.com"})

# Delete
accountDAO.delete(new_id)