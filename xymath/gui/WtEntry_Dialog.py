#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
from tkinter import *

import sys
if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    from tkSimpleDialog import Dialog
else:
    # this is only called incorrectly by pylint using python2
    from tkinter.simpledialog import Dialog


class _Dialog(Dialog):
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptions=None):
        self.initComplete = 0
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class _Wtentry(_Dialog):

    def body(self, master):
        dialogframe = Frame(master, width=320, height=200)
        dialogframe.pack()


        self.Label_1 = Label(dialogframe,text="Enter Weighting Factor for X,Y Data Point")#, width="15")
        self.Label_1.pack(anchor=NW, side=TOP)#place(x=36, y=24, width=252, height=22)

        s = 'X=%s, Y=%s'%(self.dialogOptions['x'], self.dialogOptions['y'])
        self.Xyvalue_Label = Label(dialogframe,text=s)#, width="15")
        self.Xyvalue_Label.pack(anchor=NW, side=TOP)#place(x=36, y=72, width=219, height=22)


        self.Label_Space = Label(dialogframe,text=" ")
        self.Label_Space.pack(anchor=NW, side=TOP)

        self.e_frame = Frame(dialogframe)
        self.Label_Wt = Label(self.e_frame,text="Weight =")#, width="15")
        self.Label_Wt.pack(anchor=NW, side=LEFT)#place(x=36, y=108, width=70, height=22)

        self.Wtvalue_Entry = Entry(self.e_frame)#,width="15")
        self.Wtvalue_Entry.pack(anchor=NW, side=LEFT)#place(x=96, y=108, width=96, height=21)
        self.Wtvalue_Entry_StringVar = StringVar()
        self.Wtvalue_Entry.configure(textvariable=self.Wtvalue_Entry_StringVar)
        self.Wtvalue_Entry_StringVar.set( self.dialogOptions['w'] )
        self.Wtvalue_Entry_StringVar_traceName = \
            self.Wtvalue_Entry_StringVar.trace_variable("w", self.Wtvalue_Entry_StringVar_Callback)
        
        self.e_frame.pack(anchor=NW, side=TOP)
        
        self.Wtvalue_Entry.focus_force()
        self.Wtvalue_Entry.selection_range(0, END)
        
        self.resizable(0,0) # Linux may not respect this


    def Wtvalue_Entry_StringVar_Callback(self, varName, index, mode):
        print("Wtvalue_Entry_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.Wtvalue_Entry_StringVar.get())


    def validate(self):
        self.result = {} # return a dictionary of results
    
        # >>>>>>insert any user code below this comment for section "dialog_validate"
        # set values in "self.result" dictionary for return
        # for example...
        self.result["Weight"] = self.Wtvalue_Entry.get() 
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

    def Button_1_Click(self, event):
        dialog = _Wtentry(self.master, title="Point #3 Weighting Factor", 
                          dialogOptions={'x':2.345, 'y':7.89, 'w':2.2})
        print('===============Result from Dialog====================')
        print(dialog.result)
        print('=====================================================')

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
