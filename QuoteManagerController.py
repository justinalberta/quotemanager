#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      JB
#
# Created:     28/06/2014
# Copyright:   (c) JB 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import csv
import MySQLdb
import os
import QuoteManagerModel

def main():
    pass

if __name__ == '__main__':
    main()


def uploadQuote(filePath):

    #filePath = "C:\\Users\\JB\\Desktop\\QuoteManager\\test.csv"

    if filePath == None:  #Cancels running of function if user selects Cancel
        print("No File")
        return
    else:
        (thePath,fileName) = os.path.split(filePath) #splits filepath and file name that was provided by fileFind function in QuoteManagerView

    """Uploads a new quote from a template csv file into the quoteparts table of theh QuoteManager MYSQL database. """

    print(thePath)
    print(fileName)

    os.chdir(thePath)

    InsertIt = QuoteManagerModel.dbAction()

    with open(fileName, 'rb') as f:  #read csv file
        reader = csv.reader(f)
        for row in reader:
            rowid = row[0]  #todo create better id and ensure unique (quote#,Sim,Expiry Date?)
            sim = row[1]   #todo Add check if all numbers
            cost = float(row[2]) #ensures it's a float to enter double value into db

            query = "INSERT INTO quoteparts VALUES (%s,%s,%s)" % (rowid,sim[:11],cost) #Insert id, sim, cost into table // grabs only first 11 digits of SIM

            InsertIt.dbInsert(query)

    InsertIt.dbClose()
    print("Upload Complete")





##def quoteTemplate():
##    #create quote upload template
##
##def quoteQuery():
##    #lookup individual parts quote
##
##def queryQuoteSummary():
##    #look up quote summary
##
##def editQuote():
##    #edit quote line
##
##def archiveQuote():
##    #archive quotes to different archive table
##
##def quoteCommentForm():
##    #create comment form for WPS
##
##
##