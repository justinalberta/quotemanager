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
import config

class uploadPanel(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        config.selection = 'New Quote'

        quoteNum = wx.TextCtrl(parent=self,id=-1,value="Quote Number",pos=(150,10))
        quoteSupplier = wx.TextCtrl(parent=self,id=-1,value="Supplier Number",pos=(150,40))
        quoteCustomer = wx.TextCtrl(parent=self,id=-1,value="Customer Number",pos=(150,70))
        quoteBranch = wx.TextCtrl(parent=self,id=-1,value="Branch Number",pos=(150,100))
        quoteEffDate = wx.DatePickerCtrl(parent=self,id=-1,style=wx.DP_DROPDOWN,pos=(150,180))
        quoteExpDate = wx.DatePickerCtrl(parent=self,id=-1,style=wx.DP_DROPDOWN,pos=(150,230))
        quoteSaleperson = wx.TextCtrl(parent=self,id=-1,value="Sales Person",pos=(150,130))

        def quoteHeaderUpload(qN=quoteNum,qS=quoteSupplier,qC=quoteCustomer,qB=quoteBranch,qEfD=quoteEffDate,qExD=quoteExpDate,qSp=quoteSaleperson):
            QuoteManagerController.uploadQuoteHeader(qN,qS,qC,qB,qEfD,qExD,qSp)


        def upLoadIt(event):
            self.quoteHeader.quoteHeaderUpload()
            fileFinder = fileFind() #Run by Upload button. If no file is selected, then print message and return.
            if fileFinder ==  None:
                wx.StaticText(self,-1,"No file selected",(40,100))
                return
            else:
                QuoteManagerController.uploadQuote(fileFinder,config.selection)
                wx.StaticText(self,-1,"Upload Complete",(40,100))


        def fileFind(): #Select file to be uploaded, default csv files
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
        uploadButton.Bind(wx.EVT_BUTTON, upLoadIt)
        self.Show()

    def Quit(self,event):
            self.Close()


class mainPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        mainButton = wx.Button(self,label="Main",pos=(20, 40))

class maintPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        uploadOptions = ['Part List','Customer List','Supplier List']
        uploadCombo = wx.ComboBox(self, pos=(20, 10), choices=uploadOptions,style=wx.CB_READONLY)
        uploadCombo.Bind(wx.EVT_COMBOBOX, self.onSelect)

        def upLoadIt(event):
            self.quoteHeader.quoteHeaderUpload()
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
        uploadButton.Bind(wx.EVT_BUTTON, upLoadIt)

    def onSelect(self,event): #gets option for upload type
            selection = event.GetString()                                               #<-------------------- Need to get var to
            config.selection = selection


class commentPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        quoteNum = wx.TextCtrl(parent=self,id=-1,value="Quote Number",pos=(10,10))
        commentButton = wx.Button(self,label="Generate Comments",pos=(10, 50))
        commentButton.Bind(wx.EVT_BUTTON, self.holder)

    def holder():
        pass





class menuStart(wx.Frame):

    def Quit(self,event):
        self.Close()

    def __init__(self,parent,id):
        wx.Frame.__init__(self, parent, wx.ID_ANY,"Main", size=(500,500))


        self.uploadScreen = uploadPanel(self)
        self.uploadScreen.Show()

        self.mainScreen = mainPanel(self)
        self.mainScreen.Hide()

        self.maintScreen = maintPanel(self)
        self.maintScreen.Hide()

        self.commentScreen = commentPanel(self)
        self.commentScreen.Hide()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mainScreen, 1, wx.EXPAND)
        sizer.Add(self.uploadScreen,1,wx.EXPAND)
        sizer.Add(self.maintScreen,1,wx.EXPAND)
        sizer.Add(self.commentScreen,1,wx.EXPAND)
        self.SetSizer(sizer)


        menuBar = wx.MenuBar()
        menuFile= wx.Menu()
        menuLookup = wx.Menu()
        menuMaint = wx.Menu()

        exitItem = menuFile.Append(wx.ID_EXIT,"Exit","Exit Program")
        self.Bind(wx.EVT_MENU, self.Quit,exitItem)

        commentPrint = menuFile.Append(wx.NewId(),"Comment Generator","Create Comment Report")
        self.Bind(wx.EVT_MENU,partial(self.onSwitchPanels, screen = "comment"),commentPrint)

        menuLookup.Append(wx.NewId(),"Query","Lookup Quote") #bind?
        menuLookup.Append(wx.NewId(),"Edit Part","Change Quote") #bind?

        uploadItem = menuMaint.Append(wx.NewId(),"Upload Quote","Upload New Quote")
        self.Bind(wx.EVT_MENU, partial(self.onSwitchPanels,screen="quote"),uploadItem)

        uploadMaint = menuMaint.Append(wx.NewId(),"Other Upload","Upload Data")
        self.Bind(wx.EVT_MENU, partial(self.onSwitchPanels,screen="maint"),uploadMaint)

        menuMaint.Append(wx.NewId(),"Delete","Delete Quote")

        menuBar.Append(menuFile,"File")
        menuBar.Append(menuLookup,"Lookup")
        menuBar.Append(menuMaint,"Maintenance")

        status = self.CreateStatusBar()
        self.SetMenuBar(menuBar)

    def onSwitchPanels(self,event,screen):  #Switches panels from menu selections
        self.mainScreen.Hide()
        self.uploadScreen.Hide()
        self.maintScreen.Hide()
        self.commentScreen.Hide()

        if screen == "main":
            self.mainScreen.Show()
        elif screen == "maint":
            self.maintScreen.Show()
        elif screen ==  "quote":
            self.uploadScreen.Show()
        elif screen == "comment":
            self.commentScreen.Show()

        self.Layout()


if __name__== '__main__':
    app=wx.App()
    frame = menuStart(parent=None,id=1)
    frame.Show()
    app.MainLoop()