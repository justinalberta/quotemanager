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

class Frame(wx.Frame):

    def __init__(self,parent,id):
        self.uploadScreen(parent,id)

    def uploadScreen(self,parent,id):
        wx.Frame.__init__(self,parent,id, 'Quote Manager', size =(500,500))
        uploadPanel=wx.Panel(self)
        status = self.CreateStatusBar()
        self.menuFunc(parent,id)

        def onSelect(event): #gets option for upload type
            selection = event.GetString()                                                  #<-------------------- Need to get var to
            config.selection = selection

        uploadOptions = ['New Quote','Part List','Customer List','Supplier List']
        uploadCombo = wx.ComboBox(uploadPanel, pos=(20, 10), choices=uploadOptions,style=wx.CB_READONLY)
        uploadCombo.Bind(wx.EVT_COMBOBOX, onSelect)

##        selectFileButton = wx.Button(uploadPanel,label="Select File",pos=(20,40))
##        selectFileButton.Bind(wx.EVT_BUTTON, self.fileFind)
        def upLoadIt(self):
            fileFinder = fileFind() #Run by Upload button. If no file is selected, then print message and return.
            if fileFinder ==  None:
                wx.StaticText(uploadPanel,-1,"No file selected",(40,100))
                return
            else:
                QuoteManagerController.uploadQuote(fileFinder,config.selection)
                wx.StaticText(uploadPanel,-1,"Upload Complete",(40,100))




        def fileFind(): #Select file to be uploaded, default csv files
            wildcard = "CSV Files (*.csv;)|*.csv|" \
            "All files (*.*)|*.*"
            fileFind = wx.FileDialog(self,message="Choose a file",defaultFile="",wildcard=wildcard,style=wx.OPEN)
            if fileFind.ShowModal()== wx.ID_OK:
                path = fileFind.GetPath()
                wx.StaticText(uploadPanel,-1,"File Selected: " + path,(40,80))
                return(path)
            else:
                fileFind.Destroy
            fileFind.Destroy

        uploadButton = wx.Button(uploadPanel,label="Upload",pos=(20, 40))
        uploadButton.Bind(wx.EVT_BUTTON, upLoadIt)
        #uploadButton.Bind(wx.EVT_BUTTON, partial(QuoteManagerController.uploadQuote, path ))         #filePath = 'C:\\Users\\JB\\Desktop\\QuoteManager\\test.csv'



    def menuFunc(self,parent,id):
        menuBar = wx.MenuBar()

        menuFile= wx.Menu()
        menuLookup = wx.Menu()
        menuMaint = wx.Menu()

        menuFile.Append(wx.NewId(),"Exit","Exit Program")
        menuFile.Append(wx.NewId(),"Comment Generator","Create Comment Report")

        menuLookup.Append(wx.NewId(),"Query","Lookup Quote") #bind?
        menuLookup.Append(wx.NewId(),"Edit Part","Change Quote") #bind?

        menuMaint.Append(wx.NewId(),"Upload","Upload New Quote")
        menuMaint.Append(wx.NewId(),"Archive","Archive Expired Quote")
        menuMaint.Append(wx.NewId(),"Delete","Delete Quote")

        menuBar.Append(menuFile,"File")
        menuBar.Append(menuLookup,"Lookup")
        menuBar.Append(menuMaint,"Maintenance")

        self.SetMenuBar(menuBar)






##def __init__(self,parent,id):
##        wx.Frame.__init__(self,parent,id, 'This is frame', size =(300,300))
##        panel2=wx.Panel(self)



if __name__== '__main__':
    app=wx.App()
    frame = Frame(parent=None,id=1)
    frame.Show()
    app.MainLoop()