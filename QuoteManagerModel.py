#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      JB
#
# Created:     29/06/2014
# Copyright:   (c) JB 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()



#!/usr/bin/python

import MySQLdb

class dbAction():

    def __init__(self):
        pass



    def dbConnect(self):
        host="localhost"
        user="jbates"
        password="redblue"
        dbname="QuoteManager"

        db = MySQLdb.connect(host,user,password,dbname) #create connection
        return db



    def dbInsert(self,query):

        db = self.dbConnect()

        cursor = db.cursor()
        try:
           # Execute the SQL command
           cursor.execute(query)
           # Commit your changes in the database
           db.commit()
        except:
           # Rollback in case there is any error
           db.rollback()
           raise
           print("DB error")

        db.close()



    def dbQuery(self,query):

        db = self.dbConnect()

        cursor = db.cursor()
        try:
           # Execute the SQL command
           cursor.execute(query)
           # Commit your changes in the database
           db.commit()
        except:
           # Rollback in case there is any error
           db.rollback()
           print("error")

        results = cursor.fetchall()

        db.close()

        return results




