#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      JB
#
# Created:     30/07/2014
# Copyright:   (c) JB 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

import os
import pypyodbc
import sys
import util


class dbAction():

    def dbConnect(self):

        #fileLoc = os.path.join(os.path.dirname(__file__), 'Data\config.txt')


        fileLoc = util.resource_path('Data\\config.txt')

        print(fileLoc)

        file = open(fileLoc, 'r')

        path = file.readline()

        #dbConn = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\JB\\Desktop\\BuyerToolsDB.accdb;'

        conn = pypyodbc.connect(path.strip())
        return conn

    #Uid=Admin;Pwd=;'

    def dbInsert(self,query):

        db = self.dbConnect()

        cur = db.cursor()

        try:

            cur.execute(query)

            cur.commit()

        except Exception,e:

            db.rollback()

            print("Exception - Error")
            print(e)

        db.close()


    def dbQuery(self,query):

        db = self.dbConnect()

        cur = db.cursor()
        try:
           # Execute the SQL command
           cur.execute(query)
           # Commit your changes in the database
        except Exception,e:
           # Rollback in case there is any error
           db.rollback()
           print("Exception - error")
           print (e)

        results = cur.fetchall()

        return results
        db.close()
