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


    host="localhost"
    user="jbates"
    password="redblue"
    dbname="QuoteManager"

    db = MySQLdb.connect(host,user,password,dbname) #create connection

    def __init__(self,host=host,user=user,password=password,dbname=dbname):
        pass


    def dbInsert(self,query,db=db):

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




    def dbQuery(self,query,db=db):

##        host="localhost"
##        user="jbates"
##        password="redblue"
##        dbname="QuoteManager"
##
##        db = MySQLdb.connect(host,user,password,dbname) #create connection
##        cursor = db.cursor()
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

    def dbClose(self,db=db):
        db.close()

##qq = "SELECT * FROM customer"
##
##theResults = dbase(query=qq)
##
##print (theResults[0][1])