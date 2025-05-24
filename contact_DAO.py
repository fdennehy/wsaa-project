# contact dao 
# This is a demonstration a data layer that connects to a datbase

import mysql.connector
import wsaa.deploytopythonanywhere.dbconfigpa as cfg

class contactDAO:
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

    def getAllContacts(self):
        cursor = self.getcursor()
        sql="select * from contacts"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertContactToDictionary(result))
        
        self.closeAll()
        return returnArray

    def convertContactToDictionary(self, resultLine):
        attkeys=['contact_id','account_id', 'first_name', 'last_name', 'email_address']
        contact = {}
        currentkey = 0
        for attrib in resultLine:
            contact[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return contact      

contactDAOInstance = contactDAO()