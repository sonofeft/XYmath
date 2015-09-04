#!/usr/bin/env python
# -*- coding: ascii -*-

from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
from tkinter import *
from PIL import Image, ImageTk
from xymath.gui.logo import logo_data

import webbrowser
import os

import sys
if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    from tkSimpleDialog import Dialog
else:
    # this is only called incorrectly by pylint using python2
    from tkinter.simpledialog import Dialog

here = os.path.abspath(os.path.dirname(__file__))
up_one = os.path.split( here )[0]  # Needed to find xymath development version
exec( open(os.path.join( up_one,'_version.py' )).read() )  # creates local __version__ variable

class _Dialog(Dialog):
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptions=None):
        self.initComplete = 0
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class _About(_Dialog):

    def body(self, master):
        dialogframe = Frame(master, width=610, height=498)
        dialogframe.pack()



        self.Canvas_1 = Canvas(dialogframe, width=643, height=157)
        self.Canvas_1.pack(anchor=N,side=TOP)
        
        self.photo = PhotoImage(format="gif", data=logo_data)
        self.Canvas_1.create_image(0, 0, image=self.photo, anchor=NW)


        all_about = 'XYmath is an update of a Turbo Pascal project from my youth.\n' +\
          'The above image is a screen shot of that original code.\n' +\
          '\nAuthor: Charlie Taylor' + '\n' + 'Copyright (c) 2013 Charlie Taylor' + '\nLicense:' + \
          'GPLv3'+ '\nVersion: ' + __version__+ '\nEmail: ' + \
          "charlietaylor@users.sourceforge.net"+ '\nStatus: ' + "4 - Beta"

        self.Label_1 = Label(dialogframe,text=all_about, font=("Helvetica bold", 16))
        self.Label_1.pack(anchor=NW, side=TOP, expand=1, fill=BOTH)
        
        
        # LaunchBrowser Button
        self.LaunchBrowser_Button = Button(dialogframe,text="Show XYmath Web Page", 
            font=("Helvetica bold", 16), bg='#000080', fg='#cccccc')
        self.LaunchBrowser_Button.bind("<ButtonRelease-1>", self.LaunchBrowser_Button_Click)
        self.LaunchBrowser_Button.pack(anchor=NW, side=TOP, expand=1, fill=X)
        
        self.resizable(1,1) # Linux may not respect this
        
    def LaunchBrowser_Button_Click(self, event=None): 
        webbrowser.open_new('https://sourceforge.net/p/xymath/xywiki/Home/')

    def validate(self):
        self.result = {} # return a dictionary of results

        self.result["test"] = "test message" 
        return 1

    def apply(self):
        print('apply called')

class _Testdialog(object):
    def __init__(self, master):
        frame = Frame(master, width=300, height=300)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        self.Button_1 = Button(text="Test Dialog", relief="raised", width="15")
        self.Button_1.place(x=84, y=36)
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    def Button_1_Click(self, event): #click method for component ID=1
        dialog = _About(self.master, "Test Dialog")
        print('===============Result from Dialog====================')
        print(dialog.result)
        print('=====================================================')

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
