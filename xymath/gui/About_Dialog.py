#!/usr/bin/env python
# -*- coding: ascii -*-

from Tkinter import *
from PIL import Image, ImageTk
from logo import logo_data
import StringIO
import webbrowser

from tkSimpleDialog import Dialog

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
        
        buf = StringIO.StringIO()
        buf.write( logo_data )
        buf.seek(0)

        img =  Image.open(buf)
        self.photo = ImageTk.PhotoImage(img)
        self.Canvas_1.create_image(0, 0, image=self.photo, anchor=NW)


        all_about = 'XYmath is an update of a Turbo Pascal project from my youth.\n' +\
          'The above image is a screen shot of that original code.\n' +\
          '\nAuthor: ' +__author__ + '\n' + __copyright__ + '\nLicense:' + \
          __license__+ '\nVersion: ' + __version__+ '\nEmail: ' + __email__+ '\nStatus: ' + __status__

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
        print 'apply called'

class _Testdialog:
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
        print '===============Result from Dialog===================='
        print dialog.result
        print '====================================================='

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
