from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object

from tkinter import *

class Dropdown( Frame ):

    def make_choice(self, event):
        this_choice = self.var.get()
        if self.callback:
            self.callback( self.label, this_choice )
        else:
            print(this_choice)
    
    def __init__(self, master, label, choiceL, label_width=None, callback=None, default_val=None,
        **kw):
        '''
        Make a labeled OptionMenu. 
        choiceL is a list of strings to be selected.
        Default is choiceL[0] unless default_val is specified
        '''
        Frame.__init__(*(self, master), **kw)
        self.master = master
        self.callback = callback # if supplied, called from make_choice
        self.label = label
        
        if label_width:
            self.label_obj = Label(self,text=label, width="%s"%label_width, anchor=W, justify=LEFT)
        else:
            self.label_obj = Label(self,text=label)
        self.label_obj.pack(anchor=W, side=LEFT)
        
        self.var = StringVar()
        if not default_val is None:
            self.var.set(default_val)
        else:
            self.var.set(choiceL[0])
        
        self.omenuBtn = OptionMenu(self, self.var, *choiceL, command=self.make_choice)
        self.omenuBtn.pack(anchor=NW, side=LEFT)
        
    def get_choice(self):
        return self.var.get()
            

class _Testdropdown(object):
    def __init__(self, master):
        frame = Frame(master, width=300, height=300)
        self.master = master
        
        self.DD_1 = Dropdown(master,'Test Selection', ['me','mine','you','yours'], label_width=20)
        #self.DD_1.pack(anchor=NW, side=LEFT)#, expand=True,fill=BOTH)
        self.DD_1.place(x=24, y=36)
        
        self.DD_2 = Dropdown(master,'Has Callback', ['me2','mine2','you2','yours2'],
            callback=self.dd_callback, label_width=20)
        #self.DD_1.pack(anchor=NW, side=LEFT)#, expand=True,fill=BOTH)
        self.DD_2.place(x=24, y=66)
        
        self.DD_3 = Dropdown(master,'Also Has Callback', ['me3','mine3','you3','yours3'],
            callback=self.dd_callback, label_width=20)
        #self.DD_1.pack(anchor=NW, side=LEFT)#, expand=True,fill=BOTH)
        self.DD_3.place(x=24, y=96)
        
        frame.pack()
    def dd_callback(self, label, newvalue):
        print('From callback "%s"'%label,'=',newvalue)
        print('DD_1 choice is',self.DD_1.get_choice())

def main():
    root = Tk()
    app = _Testdropdown(root)
    root.mainloop()

if __name__ == '__main__':
    main()
