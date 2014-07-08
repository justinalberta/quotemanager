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


##    def onSwitchPanels(self, event):
##        if self.uploadScreen.IsShown():
##            self.SetTitle("Upload")
##            self.uploadScreen.Hide()
##            self.mainScreen.Show()
##        else:
##            self.SetTitle("Panel One Showing")
##            self.uploadScreen.Show()
##            self.mainScreen.Hide()
##        self.Layout()

class uploadPanel(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        def onSelect(event): #gets option for upload type
            selection = event.GetString()                                                  #<-------------------- Need to get var to
            config.selection = selection

        uploadOptions = ['New Quote','Part List','Customer List','Supplier List']
        uploadCombo = wx.ComboBox(self, pos=(20, 10), choices=uploadOptions,style=wx.CB_READONLY)
        uploadCombo.Bind(wx.EVT_COMBOBOX, onSelect)

        def upLoadIt(event):
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
        #uploadButton.Bind(wx.EVT_BUTTON, partial(QuoteManagerController.uploadQuote, path ))         #filePath = 'C:\\Users\\JB\\Desktop\\QuoteManager\\test.csv'
        self.Show()

    def Quit(self,event):
            self.Close()


class mainPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        mainButton = wx.Button(self,label="Main",pos=(20, 40))


class menuStart(wx.Frame):

    def Quit(self,event):
        self.Close()


    def __init__(self,parent,id):
        wx.Frame.__init__(self, parent, wx.ID_ANY,"Main")

        uploadScreen = uploadPanel(self)

        uploadScreen.Show()
        def hideR(event):
            uploadScreen.Hide()
            self.showR()

        menuBar = wx.MenuBar()
        menuFile= wx.Menu()
        menuLookup = wx.Menu()
        menuMaint = wx.Menu()

        exitItem = menuFile.Append(wx.ID_EXIT,"Exit","Exit Program")
        self.Bind(wx.EVT_MENU, self.Quit,exitItem)
        menuFile.Append(wx.NewId(),"Comment Generator","Create Comment Report")

        menuLookup.Append(wx.NewId(),"Query","Lookup Quote") #bind?
        menuLookup.Append(wx.NewId(),"Edit Part","Change Quote") #bind?

        uploadItem = menuMaint.Append(wx.NewId(),"Upload","Upload New Quote")

        self.Bind(wx.EVT_MENU, hideR,uploadItem)
        menuMaint.Append(wx.NewId(),"Archive","Archive Expired Quote")
        menuMaint.Append(wx.NewId(),"Delete","Delete Quote")

        menuBar.Append(menuFile,"File")
        menuBar.Append(menuLookup,"Lookup")
        menuBar.Append(menuMaint,"Maintenance")

        status = self.CreateStatusBar()
        self.SetMenuBar(menuBar)



    def showR(self):
        mainf=mainPanel(self)
        mainf.Show()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mainf, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

if __name__== '__main__':
    app=wx.App()
    frame = menuStart(parent=None,id=1)
    frame.Show()
    app.MainLoop()