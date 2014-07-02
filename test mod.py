#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      JB
#
# Created:     01/07/2014
# Copyright:   (c) JB 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()


import wx
import QuoteManagerModel

q= "INSERT INTO quoteparts VALUES (5,99999999999,100.00)"
InsertIt = QuoteManagerModel.dbAction()

InsertIt.dbInsert(q)







##class Frame(wx.Frame):
##
##    def __init__(self,parent,id):
##        self.headr(parent,id)
##
##
##
##    def headr(self,parent,id):
##        wx.Frame.__init__(self,parent,id, 'My Program', size =(300,300))
##        panel=wx.Panel(self)
##        status = self.CreateStatusBar()
##
##
##        uploadButton = wx.Button(panel,label="Upload",pos=(20, 30))
##        uploadButton.Bind(wx.EVT_BUTTON,self.printIt)
##
##
##    def printIt(self,event):
##        print("Function has run")
##
##if __name__== '__main__':
##    app=wx.App()
##    frame = Frame(parent=None,id=1)
##    frame.Show()
##    app.MainLoop()