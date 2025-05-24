# account dao 
# This is a demonstration a data layer that connects to a datbase

import mysql.connector
import dbconfigpa as cfg

class accountDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.cursor.close()
        self.connection.close()
        
    def getAllAccounts(self):
        cursor = self.getcursor()
        sql="select * from account"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertAccountToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findAccountByID(self, id):
        cursor = self.getcursor()
        sql="select * from account where account_id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertAccountToDictionary(result)
        self.closeAll()
        return returnvalue

    def createAccount(self, account):
        cursor = self.getcursor()
        sql="insert into account (account_name,website) values (%s,%s)"
        values = (account.get("account_name"), account.get("website"))
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        account["account_id"] = newid
        self.closeAll()
        return account


    def updateAccount(self, id, account):
        cursor = self.getcursor()
        sql="update account set account_name= %s,website=%s WHERE account_id = %s"
        values = (account.get("account_name"), account.get("website"), id)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        return account
        
    def deleteAccount(self, id):
        cursor = self.getcursor()
        sql="delete from account where account_id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        #print("delete done")

    def convertAccountToDictionary(self, resultLine):
        attkeys=['account_id','account_name','website']
        account = {}
        currentkey = 0
        for attrib in resultLine:
            account[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return account      

accountDAOInstance = accountDAO()