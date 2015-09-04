#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import str
from builtins import object
from tkinter import *
import tkinter.messagebox

import sys
import os

if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    from tkSimpleDialog import Dialog
else:
    # this is only called incorrectly by pylint using python2
    from tkinter.simpledialog import Dialog


from xymath.two_row_col import get_xy_lists

class _Dialog(Dialog):
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptions=None):
        self.initComplete = 0
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class _Importxy(_Dialog):

    def body(self, master):
        
        self.dialogframe = Frame(master)
        self.dialogframe.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        self.listframe = Frame(self.dialogframe)

        self.Label_1 = Label(self.dialogframe, height="4", width='45',
            text="Select and Copy 2 Columns or 2 Rows\nof Numbers Onto Clipboard\n"+\
            "Click Paste Button to Replace Current Data.\n(or type ctrl-v)")
        self.Label_1.pack(anchor=N, side=TOP)


        self.Paste_Button = Button(self.dialogframe,text="Paste 2 Columns or 2 Rows", width="35", bg="#ccccff")
        self.Paste_Button.pack(anchor=N, side=TOP)
        self.Paste_Button.bind("<ButtonRelease-1>", self.Paste_Button_Click)

        # ==============================================================
        pcstdframe = Frame( self.listframe )
        stdframe = Frame( self.listframe )
        
        self.XDataLabel = Label(pcstdframe, text="XData")
        self.YDataLabel = Label(stdframe, text="YData")
        
        self.XDataLabel.pack(side=TOP)
        self.YDataLabel.pack(side=TOP)
        
        self.vsb = Scrollbar(stdframe, orient=VERTICAL)
        self.vsb.config(command=self.OnVsb)

        self.XData_Listbox_frame = pcstdframe
        self.XData_Listbox = Listbox(pcstdframe, width="20", height="20",
            selectmode="extended", yscrollcommand=self.vsb.set)
        self.XData_Listbox.pack(anchor=NW, side=TOP, fill=Y, expand=1)

        self.XData_Listbox_frame.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        self.XData_Listbox.bind("<ButtonRelease-1>", self.XData_Listbox_Click)


        self.YData_Listbox_frame = stdframe
        self.YData_Listbox = Listbox(stdframe, width="20",  height="20",
            selectmode="extended", yscrollcommand=self.vsb.set)
        self.vsb.pack(anchor=N, side=RIGHT, fill=Y, expand=1)
        self.YData_Listbox.pack(anchor=NW, side=TOP, fill=Y, expand=1)

        self.YData_Listbox_frame.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        self.YData_Listbox.bind("<ButtonRelease-1>", self.YData_Listbox_Click)
        
        self.listframe.pack(anchor=N, side=TOP, fill=Y, expand=1)
        
        self.XData_Listbox.bind("<MouseWheel>", self.OnMouseWheel)
        self.YData_Listbox.bind("<MouseWheel>", self.OnMouseWheel)
        
        self.bind_all("<Control-v>", self.Paste_Button_Click)
        
        
        # ==============================================================
        self.xL = []
        self.yL = []
        self.xName = ''
        self.yName = ''
        self.numBadPairs = 0
        
        self.resizable(1,1) # Linux may not respect this
        # >>>>>>insert any user code below this comment for section "top_of_init"


    def OnVsb(self, *args):
        self.XData_Listbox.yview(*args)
        self.YData_Listbox.yview(*args)

    def OnMouseWheel(self, event):
        self.XData_Listbox.yview("scroll", event.delta,"units")
        self.YData_Listbox.yview("scroll", event.delta,"units")

    def Paste_Button_Click(self, event):
        # start out deleting any x,y data in the list boxes
        self.XData_Listbox.delete(0, END)
        self.YData_Listbox.delete(0, END)
        
        print("executed method Paste_Button_Click")
        print('   on clip board:')
        print(self.dialogframe.clipboard_get())
        self.xL, self.yL, self.xName, self.yName, self.numBadPairs = \
            get_xy_lists( self.dialogframe.clipboard_get() )
        
        if self.xL:            
            for x,y in zip(self.xL,self.yL):
                self.XData_Listbox.insert(END, str(x))
                self.YData_Listbox.insert(END, str(y))
            

    def XData_Listbox_Click(self, event):
        print("executed method XData_Listbox_Click")
        print("current selection(s) =",self.XData_Listbox.curselection())
        labelL = []
        for i in self.XData_Listbox.curselection():
            labelL.append( self.XData_Listbox.get(i))
        print("current label(s) =",labelL)
        # use self.XData_Listbox.insert(0, "item zero")
        #     self.XData_Listbox.insert(index, "item i")
        #            OR
        #     self.XData_Listbox.insert(END, "item end")
        #   to insert items into the list box

    def YData_Listbox_Click(self, event):
        print("executed method YData_Listbox_Click")
        print("current selection(s) =",self.YData_Listbox.curselection())
        labelL = []
        for i in self.YData_Listbox.curselection():
            labelL.append( self.YData_Listbox.get(i))
        print("current label(s) =",labelL)
        # use self.YData_Listbox.insert(0, "item zero")
        #     self.YData_Listbox.insert(index, "item i")
        #            OR
        #     self.YData_Listbox.insert(END, "item end")
        #   to insert items into the list box

    # standard message dialogs... showinfo, showwarning, showerror
    def ShowInfo(self, title='Title', message='your message here.'):
        tkinter.messagebox.showinfo( title, message )
        return
    def ShowWarning(self, title='Title', message='your message here.'):
        tkinter.messagebox.showwarning( title, message )
        return
    def ShowError(self, title='Title', message='your message here.'):
        tkinter.messagebox.showerror( title, message )
        return
        
    # standard question dialogs... askquestion, askokcancel, askyesno, or askretrycancel
    # return True for OK, Yes, Retry, False for Cancel or No
    def AskYesNo(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askyesno( title, message )
    def AskOK_Cancel(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askokcancel( title, message )
    def AskRetryCancel(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askretrycancel( title, message )
        
    # return "yes" for Yes, "no" for No
    def AskQuestion(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askquestion( title, message )
    # END of standard message dialogs

    def validate(self):
        self.result = {} # return a dictionary of results
    
        # set values in "self.result" dictionary for return
        # for example...
        # self.result["age"] = self.Entry_2_StringVar.get() 


        self.result["xL"] = self.xL
        self.result["yL"] = self.yL
        self.result["xName"] = self.xName
        self.result["yName"] = self.yName
        self.result["numBadPairs"] = self.numBadPairs
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
        dialog = _Importxy(self.master, "Import X,Y Data")
        print('===============Result from Dialog====================')
        print(dialog.result)
        print('=====================================================')

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
