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
import os
import QuoteManagerModel
import config
import util

def main():
    pass

if __name__ == '__main__':
    main()


def uploadQuote(filePath,uploadType):


    if uploadType == None:
        print("No Upload Selection")
        return
    else:
        print(uploadType)

    if filePath == None:  #Cancels running of function if user selects Cancel
        print("No File")
        return
    else:
        (thePath,fileName) = os.path.split(filePath) #splits filepath and file name that was provided by fileFind function in QuoteManagerView

    """Uploads a new quote from a template csv file into the quoteparts table of the QuoteManager MYSQL database. """

    print(thePath)
    print(fileName)

    os.chdir(thePath)

    def quotepartsUpload(fileName=fileName):
        InsertIt = QuoteManagerModel.dbAction()

        with open(fileName, 'rb') as f:  #read csv file
            reader = csv.reader(f)

            for row in reader:
                quoteId = str(row[0])  #todo create better id and ensure unique (quote#,Sim,Expiry Date?)
                sim = row[1]   #todo Add check if all numbers
                part = row[2]
                cost = float(row[3]) #ensures it's a float to enter double value into db
                vendor = config.quoteSupplier

                #todo add table checks here and add missing info
                simQuery = '''SELECT partTable.sim FROM partTable WHERE partTable.sim = '%s' ''' % (sim)
                simCheckresult = InsertIt.dbQuery(simQuery)
                if len(simCheckresult) == 0:
                    simAddQuery = '''INSERT INTO partTable (sim,partNum,vendor) VALUES ('%s','%s','%s')''' % ((sim[:11]),str(part),str(vendor))
                    InsertIt.dbInsert(simAddQuery)

                query = '''INSERT INTO quotePrice VALUES (%s,%s,%s)''' % (quoteId,sim[:11],cost) #Insert id, sim, cost into table // grabs only first 11 digits of SIM

                InsertIt.dbInsert(query)
            f.close()

        print("Quote Upload Complete")

    def customerUpload(fileName=fileName): #todo add in check to ensure file proper file headers are in csv and then skip them (do for all options)
        InsertIt = QuoteManagerModel.dbAction()

        with open(fileName, 'rb') as f:  #read csv file
            reader = csv.reader(f)

            for row in reader:
                custId = row[0]
                custName = str(row[1])

                query = '''INSERT INTO customerTable VALUES (%s,'%s');''' % (custId,custName)
                InsertIt.dbInsert(query)

        print("Customer Upload Complete")

    def partsUpload(fileName=fileName): #todo add in check to ensure file proper file headers are in csv and then skip them (do for all options)
        InsertIt = QuoteManagerModel.dbAction()

        with open(fileName, 'rb') as f:  #read csv file
            reader = csv.reader(f)

            for row in reader:
                sim = row[0]
                partNumber = str(row[1])
                vendor = str(row[2])
                price = str(row[3])

                query = '''INSERT INTO partTable VALUES (%s,'%s','%s','%s');''' % (sim[:11],partNumber,vendor,price)
                InsertIt.dbInsert(query)
            f.close()
        print("Price Upload Complete")

    def supplierUpload(fileName=fileName): #todo add in check to ensure file proper file headers are in csv and then skip them (do for all options)
        InsertIt = QuoteManagerModel.dbAction()

        with open(fileName, 'rb') as f:  #read csv file
            reader = csv.reader(f)

            for row in reader:
                supplierNumber = row[0]
                print(supplierNumber)
                supplierName = str(row[1])
                print(supplierName)

                query = '''INSERT INTO supplierTable VALUES ('%s','%s');''' % (supplierNumber,supplierName)
                InsertIt.dbInsert(query)
            f.close()

        print("Supplier Upload Complete")



    if uploadType == 'New Quote':
        quotepartsUpload()
    elif uploadType =="Customer List":
        customerUpload()

    elif uploadType == "Price List":
        partsUpload()
    elif uploadType == "Supplier List":
        supplierUpload()
    else:
        print("No upload type selected")
        return




def uploadQuoteHeader(quoteNumber,quoteSupplier,quoteCustomer,quoteBranch,quoteEffDate,quoteExpDate,salesperson):
     query = '''INSERT INTO quoteSummary VALUES ('%s','%s','%s','%s','%s','%s','%s');''' % (quoteNumber,quoteSupplier,quoteCustomer,quoteBranch,quoteEffDate,quoteExpDate,salesperson)
     InsertIt = QuoteManagerModel.dbAction()
     InsertIt.dbInsert(query)


class commentPrinter():
    def __init__(self):
        pass

    def lookUp(self,quote):
        findIt = QuoteManagerModel.dbAction()
        query1 = '''SELECT qs.quoteNum,qs.supplierNum,qs.customerNum,qs.branch,qs.effDate,qs.expDate FROM quoteSummary qs WHERE qs.quoteNum='%s';''' %(quote)
        query2 = '''SELECT qp.sim,qp.price FROM quotePrice qp WHERE qp.quoteNum = '%s';''' % (quote)
        result1 = findIt.dbQuery(query1)
        result2 = findIt.dbQuery(query2)
        print(result2)

        quoteNumber = str(result1[0][0])
        quoteSupplier = str(result1[0][1])
        quoteCustomer = str(result1[0][2])
        quoteBranch = str(result1[0][3])
        quoteEffective = str(result1[0][4])
        quoteExpiry = str(result1[0][5])
        quoteExp = quoteExpiry.split()
        quoteEff = quoteEffective.split()



        rownum = 0

        ofile = open(util.resource_path('Data\Quote_Comments.csv'),"wb")
        #ofile  = open('C:\Users\JB\Desktop\Quote_Comments.csv', "wb")
        writer = csv.writer(ofile)
        for row in result2:

            if rownum == 0:
                group = 'Group'
                region = 'Region'
                branch = 'Branch'
                simMfr = 'Sim Mfr'
                simItem = 'Sim Item'
                seq = 'Seqence No'
                preset = 'Preset'
                comment = 'Comment'
                output = 'Output To PO'
                start = 'Start Date'
                end = 'End Date'

                outRow = (group,region,branch,simMfr,simItem,seq,preset,comment,output,start,end,'\r\n')
                writer.writerow(outRow)
                rownum += 1
            else:

                quoteSIM = str(row[0])
                simMfrNum = str(quoteSIM[:6])
                simItemNum = str(quoteSIM[-5:])
                quotePrice = str(row[1])
                fullComment = 'Quote: %s Cost: %s Br: %s Expiry: %s'%(quoteNumber,quotePrice,quoteBranch,str(quoteExp[0]))
                outRow = ('','',quoteBranch,simMfrNum,simItemNum,'10','',fullComment,"",str(quoteEff[0]),str(quoteExp[0]),'\r\n')
                writer.writerow(outRow)

        ofile.close()


    def export():
        pass


class priceLookup():

    def __init__(self):
        pass
    def Lookup(self,sim):
        findIt = QuoteManagerModel.dbAction()
        query = '''SELECT partTable.stockPrice FROM partTable WHERE partTable.sim = '%s' ''' % (sim)
        findItResult = findIt.dbQuery(query)
        return findItResult

    def lookupQuote(self,sim):
        findIt = QuoteManagerModel.dbAction()

        query = '''SELECT quotePrice.quoteNum, quotePrice.price, quoteSummary.branch, customerTable.customerName, quoteSummary.effDate, quoteSummary.expDate
        FROM customerTable INNER JOIN (quoteSummary INNER JOIN quotePrice ON quoteSummary.quoteNum = quotePrice.quoteNum) ON customerTable.customerNum = quoteSummary.customerNum
        WHERE (((quotePrice.sim)='%s'));''' %(sim)

        findItResult = findIt.dbQuery(query)

        return findItResult

class poCheck():

    def check(self,fileName):
        findIt = QuoteManagerModel.dbAction()
        with open(fileName, 'rb') as f:  #read csv file
                reader = csv.reader(f)

                rownum = 0

                ofile = open(util.resource_path('Data\PO_COST_REPORT.csv'),"wb")
                writer = csv.writer(ofile)
                for row in reader:

                    if rownum == 0:
                        line = 'Line'
                        sim = 'SIM'
                        case = 'Case'
                        cost = 'Cost'
                        outRow = (line,sim,case,cost,'\r\n')
                        writer.writerow(outRow)


                    elif rownum == 1:
                        pass
                    else:
                        line = str(row[33])
                        sim = str(row[35])  #todo create better id and ensure unique (quote#,Sim,Expiry Date?)
                        price = str(row[45])   #todo Add check if all numbers
                        quantity = str(row[44])
                        neg = str(row[41])

                        query = '''SELECT pt.stockPrice,pt.case FROM partTable AS pt WHERE pt.sim = '%s'; ''' %(sim)
                        poResult = findIt.dbQuery(query)

                        actualCost = (str(poResult[0][0]))
                        actualCase = (str(poResult[0][1]))

                        quoteQuery = '''SELECT qp.quoteNum, qp.price FROM quotePrice qp WHERE qp.sim = '%s';''' % (sim)
                        quoteResult = findIt.dbQuery(quoteQuery)

                        #ADD IN HERE: quote lookup, find lowest quote, create report


                        if price != actualCost:
                            costMessage = "Error: Vendor Cost is: %s" % (actualCost)
                        else:
                            costMessage = "Cost OK"

                        if (int(quantity) % int(actualCase)) == 0:
                            caseMessage = "Case OK"
                        else:
                            caseMessage = "Warning: Quantity Not Full Case"

    #todo Add Try Exception here and elsewhere

                        writer = csv.writer(ofile)
                        outRow = (line,sim,caseMessage,costMessage, '\r\n')
                        writer.writerow(outRow)
                    rownum += 1
                f.close()
                ofile.close()


