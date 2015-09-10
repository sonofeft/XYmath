#!/usr/bin/env python
# -*- coding: ascii -*-


from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
from tkinter import *
        
def str_is_float( val ):
    try:
        f = float( val )
        return True
    except:
        return False


class NonLinFitPage(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any issues.'''
        print('Leaving NonLinFitPage')
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print('Entering NonLinFitPage')
            
    def __init__(self, guiObj, pageFrame):
        
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
        
        self.constEntryWidgetL = []
        
        # make frames
        self.left_frame = Frame(pageFrame)
        self.right_frame = Frame(pageFrame)
        self.const_frame = Frame(self.left_frame)
        self.eqn_frame = Frame(self.right_frame)
        self.sum_frame = Frame(self.right_frame)

        # make radio buttons
        self.Fitby_Labelframe = LabelFrame(self.left_frame,text="Fit By:", height="132", width="189")

        self.Pcenterror_Radiobutton = Radiobutton(self.Fitby_Labelframe,text="Percent Error", 
            value="PcentStdDev", width="15", anchor=W)
        self.Pcenterror_Radiobutton.pack(anchor=NW, side=TOP)
        self.RadioGroup1_StringVar = StringVar()
        self.RadioGroup1_StringVar.set("StdDev")
        self.RadioGroup1_StringVar_traceName = self.RadioGroup1_StringVar.trace_variable("w", self.RadioGroup1_StringVar_Callback)
        self.Pcenterror_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

        self.Total_Radiobutton = Radiobutton(self.Fitby_Labelframe,text="Total Error", 
            value="StdDev", width="15", anchor=W)
        self.Total_Radiobutton.pack(anchor=NW, side=TOP)
        self.Total_Radiobutton.configure(variable=self.RadioGroup1_StringVar )
        self.Fitby_Labelframe.pack(anchor=NW, side=TOP)
        
        # show CurveFit Button
        self.Curvefit_Button = Button(self.left_frame,text="Curve Fit", width="18", bg='#ccffcc')
        self.Curvefit_Button.bind("<ButtonRelease-1>", self.Curvefit_Button_Click)
        self.Curvefit_Button.pack(anchor=NW, side=TOP)
        
        # show constants list
        self.const_frame.pack(anchor=NW, side=TOP)
        
        # show ImproveFit Button
        self.ImproveFit_Button = Button(self.left_frame,text="Improve Fit", width="18", bg='#ccffff')
        self.ImproveFit_Button.bind("<ButtonRelease-1>", self.ImproveFit_Button_Click)
        self.ImproveFit_Button.pack(anchor=NW, side=TOP)
        self.ImproveFit_Button.pack_forget()

        self.SetConst_Button = Button(self.left_frame,text="Set Constants", width="18", bg='#ccffff')
        self.SetConst_Button.bind("<ButtonRelease-1>", self.SetConst_Button_Click)
        self.SetConst_Button.pack(anchor=NW, side=TOP)
        self.SetConst_Button.pack_forget()

        # start eqn_frame
        self.YEqualsLabel = Label(self.eqn_frame, text="y =", font=("Helvetica", 16))
        self.YEqualsLabel.pack(anchor=NW, side=LEFT)
        
        self.EqnStr_Text = Text( self.eqn_frame , width="50", height="5")
        self.EqnStr_Text.pack(anchor=NW,side=LEFT, fill=X, expand=1)
        self.EqnStr_Text.insert(END, 'A*x**c')

        
        # ShowHelp Button
        self.ShowHelp_Button = Button(self.eqn_frame,text="Show\nHelp", width="7", height='5')
        self.ShowHelp_Button.bind("<ButtonRelease-1>", self.ShowHelp_Button_Click)
        self.ShowHelp_Button.pack(anchor=NW, side=LEFT)

        #slab = Label(self.eqn_frame,text="  "*20) # pin xframe and yframe to the left
        #slab.pack(anchor=E, side=LEFT)#, expand=True,fill=BOTH)
        
        self.MessagesLabel = Label(self.sum_frame, text="Messages")#, font=("Helvetica", 16))
        self.MessagesLabel.pack(anchor=NW, side=TOP)
        
        # make text resulsts area
        lbframe = Frame( self.sum_frame )
        self.Messages_Text_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Messages_Text = Text(lbframe, width="45", height="12", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Messages_Text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Messages_Text.pack(side=LEFT, fill=BOTH, expand=1)
        self.Messages_Text_frame.pack(anchor=NW, side=TOP, fill=BOTH, expand=1)

        # pack frames
        
        self.left_frame.pack(anchor=NW, side=LEFT)
        
        self.eqn_frame.pack(anchor=NW, side=TOP)
        self.sum_frame.pack(anchor=NW, side=TOP, fill=BOTH, expand=1)
        self.right_frame.pack(anchor=NW, side=LEFT, fill=BOTH, expand=1)
        
        self.ShowHelp_Button_Click()

    def EqnStr_Entry_StringVar_Callback(self, varName, index, mode):
        pass
        # >>>>>>insert any user code below this comment for section "EqnStr_Entry_StringVar_Callback"
        # replace, delete, or comment-out the following
        print("EqnStr_Entry_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.EqnStr_Entry_StringVar.get())

    
    def put_nonlin_fit_on_plot(self):
        
        XY = self.guiObj.XYjob        
        
        curveL = []        
        if (XY.dataset and XY.dataset.N > 1) or XY.nonlin_fit:

            self.guiObj.PlotWin.make_new_plot(dataset=XY.dataset, curveL=[XY.nonlin_fit], 
                title_str='Non-Linear Curve Fit')

    def ShowHelp_Button_Click(self, event=None): 
        #print 'Pressed ShowHelp Button'
        self.new_message('''Enter ONLY the Right Hand Side of Your Equation
(Assumed to be "y" equals a function of "x".  or "y=f(x)")

For example to fit the equation "y = A*x**c" Enter:
A*x**c

Notice that "x" must be lower case. Constants can be any 
mix of upper or lower case. Standard variable name rules
apply. For example legal names include 
   A, c, mu, c8, theta, myConst, ZZZ, C3H8

Do NOT include "y" in the equation's right hand side.

All constants start out with a value of 1.0 and are then
optimized with a least squares approach to find the best
values. Sometimes the optimization process will get stuck
in a local optima. If this appears to be the case, edit
the constant's values and click "Set Constants", followed
by "Improve Fit". If the equation form is a good one, this
can result in a better curve fit.

Standard functions sin, cos, tan, log, log10, exp, sqrt,
log1p, sinh, cosh and tanh are available.

Be aware that linear equations will also work correctly.
for example enter "m*x + b" to fit a straight line.

As in "Simple Fit" and "Exhaustive Fit", be sure to
select either Percent or Total Error.

Note that for some equations, divide by zero is allowed if it results in (1/infinity) which is equal to 0.0

''')
        self.ShowHelp_Button.configure(state=DISABLED,text="",width="1",relief=FLAT)

    def Curvefit_Button_Click(self, event): 
        print('Pressed Curvefit Button')
        
        rhs_eqnStr = str( self.EqnStr_Text.get(1.0, END) ).strip()
        XY = self.guiObj.XYjob
        
        self.set_nonlin_obj_constants()
        if XY.nonlin_fit:
            constDinp = XY.nonlin_fit.constD.copy()
        else:
            constDinp = None
            
            
        if "PcentStdDev" == self.RadioGroup1_StringVar.get():
            self.new_message('Fitting Non-Linear Equation to dataset with Percent Error.\n\n')
            XY.fit_dataset_to_nonlinear_eqn( run_best_pcent=1, rhs_eqnStr=rhs_eqnStr, constDinp=constDinp)
        else:
            self.new_message('Fitting Non-Linear Equation to dataset with Total Error.\n\n')
            XY.fit_dataset_to_nonlinear_eqn( run_best_pcent=0, rhs_eqnStr=rhs_eqnStr, constDinp=constDinp)
        
        # remove any constant entry widgets and pack_forget Improve Button
        self.ImproveFit_Button.pack_forget()
        self.SetConst_Button.pack_forget()
        
        for e in self.constEntryWidgetL:
            e.pack_forget()
            del(e)
        
        if XY.nonlin_fit.errorStr: # show error and quit
            self.add_to_messages( XY.nonlin_fit.errorStr )
        else:
            for c in XY.nonlin_fit.orderedConstL:
                e = Entry(self.const_frame,width="25")
                e.insert(0,'%s=%s'%(c,XY.nonlin_fit.constD[c]))
                e.pack(anchor=NW, side=TOP)
                self.constEntryWidgetL.append(e)
                
            self.add_to_messages( XY.nonlin_fit.get_full_description() )
            
            self.ImproveFit_Button.pack(anchor=NW, side=TOP)
            self.SetConst_Button.pack(anchor=NW, side=TOP)
            
            self.put_nonlin_fit_on_plot()

    def set_nonlin_obj_constants(self):
        XY = self.guiObj.XYjob
        
        for e in self.constEntryWidgetL:
            s = str(e.get())
            sL = s.split('=')
            if len(sL)==2:
                if str_is_float( sL[1] ):
                    c = str(sL[0])
                    f = float( sL[1] )
                    XY.nonlin_fit.constD[c] = f
                    

    def ImproveFit_Button_Click(self, event): 
        print('Pressed ImproveFit Button')
        
        XY = self.guiObj.XYjob
        self.set_nonlin_obj_constants()
        
        if "PcentStdDev" == self.RadioGroup1_StringVar.get():
            self.new_message("Improving Fit's Percent Error.\n\n")
            XY.nonlin_fit.fit_best_pcent = 1
            XY.nonlin_fit.fit_to_data()
        else:
            self.new_message("Improving Fit's Total Error.\n\n")
            XY.nonlin_fit.fit_best_pcent = 0
            XY.nonlin_fit.fit_to_data()

        for i,c in enumerate(XY.nonlin_fit.orderedConstL):
            e = self.constEntryWidgetL[i]
            e.delete(0, END)
            e.insert(0,'%s=%s'%(c,XY.nonlin_fit.constD[c]))
        self.add_to_messages( XY.nonlin_fit.get_full_description() )
        self.put_nonlin_fit_on_plot()


    def SetConst_Button_Click(self, event): 
        print('Pressed Set Constants Button')
        self.new_message("Defining New Constant Values.\n\n")
        
        XY = self.guiObj.XYjob
        self.set_nonlin_obj_constants()
        XY.nonlin_fit.calc_std_values()
        self.add_to_messages( XY.nonlin_fit.get_full_description() )
        self.put_nonlin_fit_on_plot()


    def RadioGroup1_StringVar_Callback(self, varName, index, mode):
        pass
        # >>>>>>insert any user code below this comment for section "RadioGroup1_StringVar_Callback"
        # replace, delete, or comment-out the following
        print("RadioGroup1_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.RadioGroup1_StringVar.get())
    
    def clear_messages(self):
        self.Messages_Text.delete(1.0, END)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show\nHelp",width="7",relief=RAISED)
        
    def add_to_messages(self, s):
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show\nHelp",width="7",relief=RAISED)
        
    def new_message(self, s):
        self.clear_messages()
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show\nHelp",width="7",relief=RAISED)
