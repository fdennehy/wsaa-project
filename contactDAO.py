# Data Layer containing functions that interact with a mysql database contact table

# Import required modules, including python anywhere database config details
import mysql.connector
import dbconfigpa as cfg

class contactDAO:
    connection =    ''
    cursor =        ''
    host =          ''
    user =          ''
    password =      ''
    database =      ''
    
    # Function to initiate and assign config values
    def __init__(self):
        self.host =      cfg.mysql['host']
        self.user =      cfg.mysql['user']
        self.password =  cfg.mysql['password']
        self.database =  cfg.mysql['database']

    # Function to assign connection and cursor
    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    # Function for closing cursor and database connection, which will be run after each SQL database function
    def closeAll(self):
        self.cursor.close()
        self.connection.close()

    # Function to return an array of all contact info
    def getAllContacts(self):
        try:
            cursor = self.getcursor()
            sql="SELECT * FROM contact"
            cursor.execute(sql)
            results = cursor.fetchall()
            returnArray = [self.convertContactToDictionary(result) for result in results]
            return returnArray
        except mysql.connector.Error as err:
            print(f"DB Error in getAllContacts: {err}")
            return None
        finally:
            self.closeAll()

    # Function to return specific contact info as a dictionary, provided contact id  
    def findContactByID(self, id):
        try:
            cursor = self.getcursor()
            sql="SELECT * FROM contact where id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            print("Raw DB row:", result) # debug
            return self.convertContactToDictionary(result) if result else None
        except mysql.connector.Error as err:
            print(f"DB Error in findContactByID: {err}")
            return None
        finally:
            self.closeAll()

    # Function to create a new contact, returing contact details
    def createContact(self, contact):
        try:
            cursor = self.getcursor()
            sql="INSERT INTO contact (account_id, first_name, last_name, email, phone, health_score) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (
                contact.get("account_id"),
                contact.get("first_name"),
                contact.get("last_name"), 
                contact.get("email"), 
                contact.get("phone"), 
                contact.get("health_score")
            )
            cursor.execute(sql, values)
            self.connection.commit()
            # assign contact id
            contact["id"] = cursor.lastrowid
            return contact
        except mysql.connector.Error as err:
            print(f"DB Error in createContact: {err}")
            return None
        finally:
            self.closeAll()

    # Function to update an existing contact, provided contact id
    def updateContact(self, id, contact):
        try:
            cursor = self.getcursor()
            sql="update contact set account_id=%s, first_name=%s,last_name=%s,email=%s, phone=%s, health_score=%s WHERE id = %s"
            values = (
                contact.get("account_id"),
                contact.get("first_name"),
                contact.get("last_name"), 
                contact.get("email"), 
                contact.get("phone"), 
                contact.get("health_score"),
                id
            )
            cursor.execute(sql, values)
            self.connection.commit()
            return contact
        except mysql.connector.Error as err:
            print(f"DB Error in updateContact: {err}")
            return None
        finally:
            self.closeAll()

    # Function to delete an existing contact, provided contact id    
    def deleteContact(self, id):
        try:
            cursor = self.getcursor()
            sql="delete from contact where id = %s"
            cursor.execute(sql, (id,))
            self.connection.commit()
            return{"status": "deleted", "id": id}
        except mysql.connector.Error as err:
            print(f"DB Error in deleteContact: {err}")
            return None
        finally:
            self.closeAll()

    # Function to hydrate database with dummy data.
    def dummyContactDataInsert(self, contact):
        try:
            cursor = self.getcursor()
            sql = "INSERT INTO contact (account_id, first_name, last_name, email, phone, health_score) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (
                contact["account_id"],
                contact["first_name"],
                contact["last_name"], 
                contact["email"], 
                contact["phone"], 
                contact["health_score"]    
            )
            cursor.execute(sql, values)
            self.connection.commit()
            return{"status": "dummy contact data inserted"}
        except mysql.connector.Error as err:
            print(f"DB Error in dummyContactDataInsert: {err}")
            return None
        finally:
            self.closeAll()

    # Function to convert contact details to a dictionary object, making JSON responses clean
    def convertContactToDictionary(self, resultLine):
        attkeys=['id', 'first_name', 'last_name', 'email', 'phone', 'health_score','account_id']
        contact = {}
        currentkey = 0
        for attrib in resultLine:
            contact[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return contact      

contactDAOInstance = contactDAO()