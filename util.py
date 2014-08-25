#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      JB
#
# Created:     08/08/2014
# Copyright:   (c) JB 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

import wx
import sys
import os

def fileFind(parent): #Select file to be uploaded, default csv files
    wildcard = "CSV Files (*.csv;)|*.csv|" \
    "All files (*.*)|*.*"
    fileFind = wx.FileDialog(parent,message="Choose a file",defaultFile="",wildcard=wildcard,style=wx.OPEN)
    if fileFind.ShowModal()== wx.ID_OK:
        path = fileFind.GetPath()
        wx.StaticText(parent,-1,"File Selected: " + path,(10,250))
        return(path)
    else:
        fileFind.Destroy
    fileFind.Destroy

def resource_path(relative_path):
    '''Get absolute path to resource, works for dev and for PyInstaller '''
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

