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

def main():
    pass

if __name__ == '__main__':
    main()


import wx
import QuoteManagerController
from functools import partial
from datetime import datetime
import config

class uploadPanel(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        self.initialPanel()


    def initialPanel(self):
        config.selection = 'New Quote'
        def valUpdate(event):
            config.quoteNum = quoteNum.GetValue()
            config.quoteSupplier = quoteSupplier.GetValue()
            config.quoteCustomer = quoteCustomer.GetValue()
            config.quoteBranch = quoteBranch.GetValue()
            config.quoteEffDate = quoteEffDate.GetValue()
            config.quoteExpDate = quoteExpDate.GetValue()
            config.quoteSalesperson = quoteSaleperson.GetValue()
            self.upLoadIt()

        wx.StaticText(self,-1,"Quote Number:",(150,12))
        quoteNum = wx.TextCtrl(parent=self,id=-1,value="",pos=(280,10))
        wx.StaticText(self,-1,"Supplier Number:",(150,45))
        quoteSupplier = wx.TextCtrl(parent=self,id=-1,value="",pos=(280,40))
        wx.StaticText(self,-1,"Customer Number:",(150,75))
        quoteCustomer = wx.TextCtrl(parent=self,id=-1,value="",pos=(280,70))
        wx.StaticText(self,-1,"Branch Number:",(150,105))
        quoteBranch = wx.TextCtrl(parent=self,id=-1,value="",pos=(280,100))
        wx.StaticText(self,-1,"Sales Person:",(150,135))
        quoteSaleperson = wx.TextCtrl(parent=self,id=-1,value="",pos=(280,130))
        wx.StaticText(self,-1,"Effective Date:",(150,170))
        quoteEffDate = wx.DatePickerCtrl(parent=self,id=-1,style=wx.DP_DROPDOWN,pos=(280,165))
        wx.StaticText(self,-1,"Expiry Date:",(150,200))
        quoteExpDate = wx.DatePickerCtrl(parent=self,id=-1,style=wx.DP_DROPDOWN,pos=(280,195))


        uploadButton = wx.Button(self,label="Upload",pos=(20, 40))
        uploadButton.Bind(wx.EVT_BUTTON,valUpdate)
        self.Show()


    def upLoadIt(self):

        expDate = datetime.fromtimestamp(config.quoteExpDate.GetTicks())
        effDate = datetime.fromtimestamp(config.quoteEffDate.GetTicks())

        #todo make it an object
        QuoteManagerController.uploadQuoteHeader(str(config.quoteNum),str(config.quoteSupplier),str(config.quoteCustomer),str(config.quoteBranch),effDate,expDate,str(config.quoteSalesperson))
        fileFinder = self.fileFind() #Run by Upload button. If no file is selected, then print message and return.
        if fileFinder ==  None:
            wx.StaticText(self,-1,"No file selected",(10,220))
            return
        else:
            QuoteManagerController.uploadQuote(fileFinder,config.selection)
            wx.StaticText(self,-1,"Upload Complete",(10,235))


    def fileFind(self): #Select file to be uploaded, default csv files
        wildcard = "CSV Files (*.csv;)|*.csv|" \
        "All files (*.*)|*.*"
        fileFind = wx.FileDialog(self,message="Choose a file",defaultFile="",wildcard=wildcard,style=wx.OPEN)
        if fileFind.ShowModal()== wx.ID_OK:
            path = fileFind.GetPath()
            wx.StaticText(self,-1,"File Selected: " + path,(10,250))
            return(path)
        else:
            fileFind.Destroy
        fileFind.Destroy


class pricePanel(wx.Panel):
        '''Queries the cost and quote of a SIM'''
        def __init__(self,parent):
            wx.Panel.__init__(self, parent=parent)
            self.initialPanel()


        def initialPanel(self):
            def priceCheck(event):
                sim = priceLookup.GetValue()
                priceQuery = QuoteManagerController.priceLookup()
                simPrice = priceQuery.Lookup(sim)
                if simPrice == []:
                    wx.StaticText(self,-1,'No Cost Found',(10,80))
                else:
                    wx.StaticText(self,-1,'Stock Cost: ' + '$'+'%s'%(str(simPrice[0][0])),(10,80))
                simQuote = priceQuery.lookupQuote(sim)
                if simQuote == []:
                    wx.StaticText(self,-1,'No Quotes Found',(10,100))

                else:

                    height = 100
                    quoteQue = 0
                    effDate = str(simQuote[quoteQue][4])
                    effDateSplit = effDate.split()
                    expDate = str(simQuote[quoteQue][5])
                    expDateSplit = expDate.split()

                    for q in range(len(simQuote)):

                        wx.StaticText(self,-1,
                        'Quote Number: %s '%(str(simQuote[quoteQue][0])) +
                        '|  Quote Cost  $' + '%s '%(str(simQuote[quoteQue][1])) +
                        '|  Branch: ' + '%s '%(str(simQuote[quoteQue][2])) +
                        '|  Customer: ' + '%s '%(str(simQuote[quoteQue][3])) +
                        '|  Effective Date:' + ' %s '%(effDateSplit[0]) +
                        '|  Expiry Date: ' + '%s '%(expDateSplit[0])
                        ,(10,height))

                        quoteQue += 1
                        height += 20



            wx.StaticText(self,-1,"SIM:",(10,12))
            priceLookup = wx.TextCtrl(parent=self,id=-1,value="",pos=(50,10))
            priceButton = wx.Button(self,label="Query Price",pos=(10, 40))
            priceButton.Bind(wx.EVT_BUTTON,priceCheck)



class mainPanel(wx.Panel):
    '''Introduction screen to program'''
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        wx.StaticText(self,-1,"Welcome to the Buyer Utilities Program - Here to assist daily purchasing activities",(10,10))


class maintPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        uploadOptions = ['Price List','Customer List','Supplier List']
        uploadCombo = wx.ComboBox(self, pos=(20, 10), choices=uploadOptions,style=wx.CB_READONLY)
        uploadCombo.Bind(wx.EVT_COMBOBOX, self.onSelect)

        def upLoadIt(event):
            fileFinder = fileFind() #Run by Upload button. If no file is selected, then print message and return.
            if fileFinder ==  None:
                wx.StaticText(self,-1,"No file selected",(40,100))
                return
            else:
                QuoteManagerController.uploadQuote(fileFinder,config.selection)
                wx.StaticText(self,-1,"Upload Complete",(40,100))


        def fileFind(): #Select file to be uploaded, default csv files                 #<---------------------- break out file upload and use in one callable function
            wildcard = "CSV Files (*.csv;)|*.csv|" \
            "All files (*.*)|*.*"
            fileFind = wx.FileDialog(self,message="Choose a file",defaultFile="",wildcard=wildcard,style=wx.OPEN)
            if fileFind.ShowModal()== wx.ID_OK:
                path = fileFind.GetPath()
                wx.StaticText(self,-1,"File Selected: " + path,(40,80))
                return(path)
            else:
                fileFind.Destroy
            fileFind.Destroy
        uploadButton = wx.Button(self,label="Upload",pos=(20, 40))
        uploadButton.Bind(wx.EVT_BUTTON,upLoadIt)


    def onSelect(self,event): #gets option for upload type
            selection = event.GetString()                                               #<-------------------- Need to get var to
            config.selection = selection


class commentPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        def initiate(event):
            quote=quoteNum.GetValue()
            self.commentBuilder(quote)
        wx.StaticText(self,-1,"Quote Number",(10,12))
        quoteNum = wx.TextCtrl(parent=self,id=-1,value="",pos=(105,10))
        commentButton = wx.Button(self,label="Generate Comments",pos=(10, 50))
        commentButton.Bind(wx.EVT_BUTTON,initiate)


    def commentBuilder(self,quote):
        generateComments = QuoteManagerController.commentPrinter()
        generateComments.lookUp(quote)


class poCheckPanel(wx.Panel):
        def __init__(self,parent):
            wx.Panel.__init__(self, parent=parent)
            checkButton = wx.Button(self,label="Check PO",pos=(20, 40))
            checkButton.Bind(wx.EVT_BUTTON,self.startCheck)

        def fileFind(self):
            wildcard = "CSV Files (*.csv;)|*.csv|" \
            "All files (*.*)|*.*"
            fileFind = wx.FileDialog(self,message="Choose a file",defaultFile="",wildcard=wildcard,style=wx.OPEN)
            if fileFind.ShowModal()== wx.ID_OK:
                path = fileFind.GetPath()
                wx.StaticText(self,-1,"File Selected: " + path,(40,80))
                return(path)
            else:
                self.startCheck(fileFind)
                fileFind.Destroy
            fileFind.Destroy


        def startCheck(self,event):
            fileFinder = self.fileFind() #Run by Upload button. If no file is selected, then print message and return.
            if fileFinder ==  None:
                wx.StaticText(self,-1,"No file selected",(10,220))
                return
            else:
                checker = QuoteManagerController.poCheck()
                checker.check(fileFinder)
                wx.StaticText(self,-1,"Purchase Order Checked",(10,135))


class expeditePanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)



class menuStart(wx.Frame):

    def Quit(self,event):
        self.Close()

    def __init__(self,parent,id):
        wx.Frame.__init__(self, parent, wx.ID_ANY,"Buyer Utilities - Version Alpha 0.0.1", size=(1000,500))

        # this starts up the main screen, initates the others and hides them
        self.uploadScreen = uploadPanel(self)
        self.uploadScreen.Hide()

        self.mainScreen = mainPanel(self)
        self.mainScreen.Show()

        self.maintScreen = maintPanel(self)
        self.maintScreen.Hide()

        self.commentScreen = commentPanel(self)
        self.commentScreen.Hide()

        self.priceScreen = pricePanel(self)
        self.priceScreen.Hide()

        self.poCheckScreen = poCheckPanel(self)
        self.poCheckScreen.Hide()

        self.expediteScreen = expeditePanel(self)
        self.expediteScreen.Hide()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mainScreen, 1, wx.EXPAND)
        sizer.Add(self.uploadScreen,1,wx.EXPAND)
        sizer.Add(self.maintScreen,1,wx.EXPAND)
        sizer.Add(self.commentScreen,1,wx.EXPAND)
        sizer.Add(self.priceScreen,1,wx.EXPAND)
        sizer.Add(self.poCheckScreen,1,wx.EXPAND)
        sizer.Add(self.expediteScreen,1,wx.EXPAND)
        self.SetSizer(sizer)


        menuBar = wx.MenuBar()
        menuFile= wx.Menu()
        menuLookup = wx.Menu()
        #menuExped = wx.Menu()
        menuMaint = wx.Menu()
        menuOther = wx.Menu()

        exitItem = menuFile.Append(wx.ID_EXIT,"Exit","Exit Program")
        self.Bind(wx.EVT_MENU, self.Quit,exitItem)

        commentPrint = menuOther.Append(wx.NewId(),"Comment Generator","Inactive")
        self.Bind(wx.EVT_MENU,partial(self.onSwitchPanels, screen = "comment"),commentPrint)

##        expediteOrder = menuExped.Append(wx.NewId(),"Expedite","Inactive")
##        self.Bind(wx.EVT_MENU,partial(self.onSwitchPanels, screen = "expedite"),expediteOrder)

        priceQuery = menuLookup.Append(wx.NewId(),"Price Lookup","Look Up Price & Quote")
        self.Bind(wx.EVT_MENU, partial(self.onSwitchPanels,screen="price"),priceQuery)

        poCheck = menuLookup.Append(wx.NewId(),"PO Price Check","Ensure Accurate Pricing On PO - Inactive")
        self.Bind(wx.EVT_MENU, partial(self.onSwitchPanels,screen="poCheck"),poCheck)

        uploadItem = menuMaint.Append(wx.NewId(),"Upload Quote","Upload New Quote")
        self.Bind(wx.EVT_MENU, partial(self.onSwitchPanels,screen="quote"),uploadItem)

        uploadMaint = menuMaint.Append(wx.NewId(),"Master Data Upload","Upload Master Data")
        self.Bind(wx.EVT_MENU, partial(self.onSwitchPanels,screen="maint"),uploadMaint)

        menuMaint.Append(wx.NewId(),"Delete Quote","Inactive")

        menuBar.Append(menuFile,"File")
        menuBar.Append(menuLookup,"Price Query")
        #menuBar.Append(menuExped,"Expedite Orders")
        menuBar.Append(menuMaint,"Maintenance")
        menuBar.Append(menuOther,"Other")

        status = self.CreateStatusBar()
        self.SetMenuBar(menuBar)

    def onSwitchPanels(self,event,screen):  #Switches panels from menu selections
        self.mainScreen.Hide()
        self.uploadScreen.Hide()
        self.maintScreen.Hide()
        self.commentScreen.Hide()
        self.priceScreen.Hide()
        self.poCheckScreen.Hide()
        self.expediteScreen.Hide()

        if screen == "main":
            self.mainScreen.Show()
        elif screen == "maint":
            self.maintScreen.Show()
        elif screen ==  "quote":
            self.uploadScreen.Show()
        elif screen == "comment":
            self.commentScreen.Show()
        elif screen == "price":
            self.priceScreen.Show()
        elif screen == "poCheck":
            self.poCheckScreen.Show()
        elif screen == "expedite":
            self.expediteScreen.Show()

        self.Layout()


if __name__== '__main__':
    app=wx.App()
    frame = menuStart(parent=None,id=1)
    frame.Show()
    app.MainLoop()