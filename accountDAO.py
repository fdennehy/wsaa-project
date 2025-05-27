# Data Layer containing functions that interact with a mysql databased

# Import required modules, including python anywhere database config details
import mysql.connector
import dbconfigpa as cfg

class accountDAO:
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
    
    # Function to return an array of all account info
    def getAllAccounts(self):
        try:
            cursor = self.getcursor()
            sql="SELECT * FROM account"
            cursor.execute(sql)
            results = cursor.fetchall()
            returnArray = [self.convertAccountToDictionary(result) for result in results]
            return returnArray
        except mysql.connector.Error as err:
            print(f"DB Error in getAllAccounts: {err}")
            return None
        finally:
            self.closeAll()

    # Function to return specific account info as a dictionary, provided account id  
    def findAccountByID(self, id):
        try:
            cursor = self.getcursor()
            sql="SELECT * FROM account where id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return self.convertAccountToDictionary(result) if result else None
        except mysql.connector.Error as err:
            print(f"DB Error in findAccountByID: {err}")
            return None
        finally:
            self.closeAll()

    # Function to create a new account, returing account details
    def createAccount(self, account):
        try:
            cursor = self.getcursor()
            sql="INSERT INTO account (name, website, revenue, region) VALUES (%s,%s,%s,%s)"
            values = (
                account.get("name"), 
                account.get("website"), 
                account.get("revenue"), 
                account.get("region")
            )
            cursor.execute(sql, values)
            self.connection.commit()
            # assign account id
            account["id"] = cursor.lastrowid
            return account
        except mysql.connector.Error as err:
            print(f"DB Error in createAccount: {err}")
            return None
        finally:
            self.closeAll()

    # Function to update an existing account, provided account id
    def updateAccount(self, id, account):
        try:
            cursor = self.getcursor()
            sql="update account set name= %s,website=%s, revenue=%s, region=%s WHERE id = %s"
            values = (
                account.get("name"), 
                account.get("website"), 
                account.get("revenue"), 
                account.get("region"), 
                id
            )
            cursor.execute(sql, values)
            self.connection.commit()
            return account
        except mysql.connector.Error as err:
            print(f"DB Error in updateAccount: {err}")
            return None
        finally:
            self.closeAll()

    # Function to delete an existing account, provided account id    
    def deleteAccount(self, id):
        try:
            cursor = self.getcursor()
            sql = "DELETE FROM account WHERE id = %s"
            cursor.execute(sql, (id,))
            self.connection.commit()
            
            if cursor.rowcount == 0:
                return None  # No rows deleted — account not found
            else:
                return {"status": "deleted", "id": id}
        except mysql.connector.Error as err:
            print(f"DB Error in deleteAccount: {err}")
            return None
        finally:
            self.closeAll()
        
    # Function to delete all data from account table with nothing returned.
    # *Warning to be added on front end re use of this 'WIPE' function*
    def deleteAllAccounts(self):
        try:
            cursor = self.getcursor()
            sql="DELETE FROM account"
            cursor.execute(sql)
            self.connection.commit()
            return{"status": "all records deleted"}
        except mysql.connector.Error as err:
            print(f"DB Error in deleteAllAccounts: {err}")
            return None
        finally:
            self.closeAll()

    # Function to hydrate database with dummy data.
    def dummyAccountDataInsert(self):
        try:
            cursor = self.getcursor()
            sql = """
            INSERT INTO account (name, website, revenue, region) VALUES 
            ('Acme Corporation', 'https://www.acme.com', '1000', 'Asia'), 
            ('Globex Industries', 'https://www.globex.com', '200', 'South America'), 
            ('Initech', 'https://www.initech.com', '500', 'Europe'),
            ('Stark Enterprises', 'https://www.starkenterprises.com', '750', 'North America'),
            ('Wayne Enterprises', 'https://www.wayneenterprises.com', '750', 'Australia')
            """
            cursor.execute(sql)
            self.connection.commit()
            return{"status": "dummy account data inserted"}
        except mysql.connector.Error as err:
            print(f"DB Error in dummyAccountDataInsert: {err}")
            return None
        finally:
            self.closeAll()

    # Function to retrieve average health scores per account
    def avgAccountHealthScore(self):
        try:
            cursor = self.getcursor()
            sql = """
            SELECT a.name AS account_name, 
            ROUND(AVG(c.health_score), 2) AS avg_health_score
            FROM account a
            JOIN contact c ON a.id = c.account_id
            GROUP BY a.id
            ORDER BY avg_health_score DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"DB Error in avgAccountHealthScore: {err}")
            return None
        finally:
            self.closeAll()

    # Function to convert account details to a dictionary object, making JSON responses clean
    def convertAccountToDictionary(self, resultLine):
        attkeys=['id','name','website', 'revenue', 'region']
        account = {}
        currentkey = 0
        for attrib in resultLine:
            account[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return account      

accountDAOInstance = accountDAO()