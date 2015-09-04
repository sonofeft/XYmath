from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
import sys, os
from tkinter import *

import xymath.source_python
import xymath.source_fortran
import xymath.source_excel

class CodeGenPage(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any issues.'''
        print('Leaving CodeGenPage')
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print('Entering CodeGenPage')
        XY = self.guiObj.XYjob
            
        self.Listbox_1.delete(0, END)
        
        if XY.nonlin_fit:
            self.equationL = [XY.nonlin_fit]
            self.Listbox_1.insert(END, XY.nonlin_fit.name )
        else:
            self.equationL = []
        
        for pagename in ['Simple Fit','Exhaustive Fit']:
            selected_linfitL = self.guiObj.pageD[pagename].selected_linfitL
            for n,i in enumerate(selected_linfitL):
                linfit = self.guiObj.linear_fitL[i]
                self.Listbox_1.insert(END, linfit.name )
                self.equationL.append( linfit )
        
        for spline in self.guiObj.selected_spline_objL:
            self.Listbox_1.insert(END, spline.name )
            self.equationL.append( spline )
            
        self.special_title = 'Math Functions' # for putting annotations on plot
        self.specialPtL = None
        
        if len(self.equationL)>0:
            self.Listbox_1.select_set(0)
            self.put_equation_on_plot()
        

            
    def __init__(self, guiObj, pageFrame):
        
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
        # make frames
        self.main_frame = Frame(pageFrame)
        
        self.top_f = Frame(self.main_frame)
        
        self.select_f = Frame(self.top_f)
        self.right_f = Frame(self.top_f)
        self.far_right_f = Frame(self.right_f)

        self.Select_Label = Label(self.select_f,text="Select Curve", width="15")
        self.Select_Label.pack(anchor=NW, side=TOP)


        # Make Radio Group for Language Selection
        self.Language_Labelframe = LabelFrame(self.right_f ,text="Select Language:", height="132", width="189")
        
        self.Python_Radiobutton = Radiobutton(self.Language_Labelframe,text="Python", 
            value="Python", width="15", anchor=NW)
        self.Python_Radiobutton.pack(anchor=NW, side=TOP)
        self.RadioGroup1_StringVar = StringVar()
        self.RadioGroup1_StringVar.set("Python")
        self.RadioGroup1_StringVar_traceName = self.RadioGroup1_StringVar.trace_variable("w", self.RadioGroup1_StringVar_Callback)
        self.Python_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

        self.FORTRAN_Radiobutton = Radiobutton(self.Language_Labelframe,text="FORTRAN 77", 
            value="FORTRAN 77", width="15", anchor=NW)
        self.FORTRAN_Radiobutton.pack(anchor=NW, side=TOP)
        self.FORTRAN_Radiobutton.configure(variable=self.RadioGroup1_StringVar )
        

        self.Excel_Radiobutton = Radiobutton(self.Language_Labelframe,text="Excel", 
            value="Excel", width="15", anchor=NW)
        self.Excel_Radiobutton.pack(anchor=NW, side=TOP)
        self.Excel_Radiobutton.configure(variable=self.RadioGroup1_StringVar )
        
        
        self.Language_Labelframe.pack(anchor=NW, side=TOP)

        
        # make text results area
        lbframe = Frame( self.main_frame )
        self.Messages_Text_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Messages_Text = Text(lbframe,  yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Messages_Text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Messages_Text.pack(anchor=NW, side=LEFT, fill=BOTH, expand=1)
        
        
        # ShowHelp Button
        self.ShowHelp_Button = Button(self.far_right_f,text="Show Help", width="15")
        self.ShowHelp_Button.bind("<ButtonRelease-1>", self.ShowHelp_Button_Click)
        
        # Clipboard Button
        self.Clipboard_Button = Button(self.far_right_f,text="Put Source on\nClipboard", width="18")
        self.Clipboard_Button.bind("<ButtonRelease-1>", self.Clipboard_Button_Click)
        
        # GenCode Button
        self.GenCode_Button = Button(self.far_right_f,text="Generate Code", width="18", bg='#ccffcc')
        self.GenCode_Button.bind("<ButtonRelease-1>", self.GenCode_Button_Click)


        lbframe = Frame( self.select_f )
        self.Listbox_1_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Listbox_1 = Listbox(lbframe, width="35", height='10', exportselection=0,
            selectmode="normal", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Listbox_1.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Listbox_1.pack(side=LEFT, fill=BOTH, expand=1)

        self.Listbox_1_frame.pack(anchor=NW, side=TOP, expand=True,fill=Y)
        self.Listbox_1.bind("<ButtonRelease-1>", self.Listbox_1_Click)
        
        
        self.select_f.pack(anchor=NW, side=LEFT, expand=True,fill=Y)
        
        self.GenCode_Button.pack(anchor=NW, side=LEFT)
        slab = Label(self.far_right_f,text=" ") # pin xframe and yframe to the left
        slab.pack(anchor=NW, side=LEFT, expand=True, fill=X)
        
        self.ShowHelp_Button.pack(anchor=NE, side=LEFT)
        self.Clipboard_Button.pack(anchor=NE, side=LEFT)
        self.far_right_f.pack(anchor=NW, side=TOP, fill=X, expand=1)
        
        self.right_f.pack(anchor=NW, side=LEFT, fill=BOTH, expand=1)
        self.top_f.pack(anchor=NW, side=TOP)
        self.Messages_Text_frame.pack(anchor=NW, side=TOP, fill=BOTH, expand=1)
        self.main_frame.pack(anchor=NW, side=LEFT, fill=BOTH, expand=1)
        
        self.ShowHelp_Button_Click()


    def GenCode_Button_Click(self, event=None): 
        print('Pressed GenCode Button')
        self.new_message('')
        
        if self.equationL:
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]
            
            language = self.RadioGroup1_StringVar.get()
            if language.startswith(b'Python'):
                src = xymath.source_python.make_fit_func_src(obj)
            elif language.startswith(b'FORTRAN'):
                src = xymath.source_fortran.make_fit_func_src(obj)
            else:
                did_good = xymath.source_excel.make_fit_excel(obj)
                if did_good:
                    src = 'Excel launched...'
                else:
                    src = 'ERROR launching Excel...'
            self.new_message( src )

    def Clipboard_Button_Click(self, event=None): 
        contents = self.Messages_Text.get(1.0, END)
        #print contents
        self.pageFrame.clipboard_clear()
        self.pageFrame.clipboard_append( contents )

    def ShowHelp_Button_Click(self, event=None): 
        #print 'Pressed ShowHelp Button'
        self.new_message('''To Generate Code for the curve fit:
        
1) Select the desired curve
2) Select the desired language
3) Press "Generate Code" button

This text box will be filled with the desired code which can then be copied and pasted into any text editor.

When the "Copy to Clipboard" button appears, click it to place the source code on the computers clipboard for pasting into a text editor.

If Excel is selected, Excel will be launched and populated with the curve data.

All too often, the results of a curve fit are buried deep in an application's source code without sufficient documentation to recreate, verify or update the equation. The source code generated by XYmath will answer those needs.

Another often neglected aspect of using curve fits is enforcing the fit's range of applicability. The source code generated by XYmath will print warnings if the curve fit is called with an x value outside of the x data range.

Compiled FORTRAN can be imported into python through the use of the f2py utility that comes with numpy. The XYmath-generated FORTRAN code contains comments("cf2py") that help with the use of the f2py.

For example: 
python.exe -c "from numpy.f2py import main; main()" cfit.f -m cfit -h cfit.pyf
will create an f2py definition file called "cfit.pyf" from a FORTRAN source file called "cfit.f".

python.exe -c "from numpy.f2py import main; main()" cfit.pyf cfit.f 
will create a file called "cfit.pyd" that python can import with "import cfit"

See the f2py documentation for generating pyf and pyd files. Your machine may need special options such as "-c --compiler=mingw32" and/or "--fcompiler=gnu95" to define your FORTRAN compiler.
''')
        self.ShowHelp_Button.configure(state=DISABLED,text="",width="1",relief=FLAT)
        self.Clipboard_Button.configure(state=DISABLED,text="",width="1",relief=FLAT)

    
    def clear_messages(self):
        self.Messages_Text.delete(1.0, END)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show Help",width="15",relief=RAISED)
        self.Clipboard_Button.configure(state=NORMAL,text="Put Source on\nClipboard",width="15",relief=RAISED)
        
    def add_to_messages(self, s):
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show Help",width="15",relief=RAISED)
        self.Clipboard_Button.configure(state=NORMAL,text="Put Source on\nClipboard",width="15",relief=RAISED)
        
    def new_message(self, s):
        self.clear_messages()
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show Help",width="15",relief=RAISED)
        self.Clipboard_Button.configure(state=NORMAL,text="Put Source on\nClipboard",width="15",relief=RAISED)

    def Listbox_1_Click(self, event): #click method for component ID=2
        print("executed method Listbox_1_Click")
        print("current selection(s) =",self.Listbox_1.curselection())
        labelL = []
        for i in self.Listbox_1.curselection():
            labelL.append( self.Listbox_1.get(i))
        print("current label(s) =",labelL)
        self.put_equation_on_plot()

    
    def put_equation_on_plot(self, integFill=None):
        
        if len(self.Listbox_1.curselection()):
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]
            
            XY = self.guiObj.XYjob
                        
            curveL = [obj]
            self.guiObj.PlotWin.make_new_plot(dataset=XY.dataset, curveL=curveL, 
                title_str='Code Generation Curve')


    def RadioGroup1_StringVar_Callback(self, varName, index, mode):
        pass
        # >>>>>>insert any user code below this comment for section "RadioGroup1_StringVar_Callback"
        # replace, delete, or comment-out the following
        print("RadioGroup1_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.RadioGroup1_StringVar.get())
