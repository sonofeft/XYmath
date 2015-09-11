from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import map
from builtins import object

from tkinter import *

class SimplePage(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any XYjob issues.'''
        print('Leaving Simple Fit')
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print('Entering Simple Fit')

    #def __init__(self, master, pageFrame):
    def __init__(self, guiObj, pageFrame):
        
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
        
        self.selected_linfitL = []
        
        self.top_frame = Frame(pageFrame)
        self.bot_frame = Frame(pageFrame)
        
        self.listframe = Frame(self.top_frame)
        self.choiceframe = Frame(self.top_frame)
        
        # set up choiceframe
        self.Curvefit_Button = Button(self.choiceframe,text="Curve Fit", width="18", bg='#ccffcc')
        self.Curvefit_Button.bind("<ButtonRelease-1>", self.Curvefit_Button_Click)

        self.Fitby_Labelframe = LabelFrame(self.choiceframe,text="Fit By:", height="132", width="189")

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
        
        # Number of terms Spinbox
        self.NTermsLabel = Label(self.choiceframe, text="Max Terms")
        self.NTermsStringVar = StringVar(value="4")
        self.NtermsSpinbox = Spinbox(self.choiceframe, from_=1, to=4, textvariable=self.NTermsStringVar)
        
        self.Btn_Space = Label(self.choiceframe,text=" ")
        
        self.ShowHelpButton = Button(self.choiceframe,text="Show Help", width="18")
        self.ShowHelpButton.bind("<ButtonRelease-1>", self.ShowHelp_Button_Click)
        

        self.Fitby_Labelframe.pack(anchor=NW, side=TOP)
        self.Curvefit_Button.pack(anchor=NW, side=TOP)
        
        self.NTermsLabel.pack(anchor=NW, side=TOP)
        self.NtermsSpinbox.pack(anchor=NW, side=TOP)

        self.Btn_Space.pack(anchor=NW, side=TOP, fill=Y, expand=1)
        self.ShowHelpButton.pack(anchor=SE, side=BOTTOM)

        self.choiceframe.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        
        # set up list boxes

        #lbframe = Frame( self.listframe )
        eqnframe = Frame( self.listframe )
        pcstdframe = Frame( self.listframe )
        stdframe = Frame( self.listframe )
        
        self.EqnLabel = Label(eqnframe, text="Equations")
        self.PcentStdDevLabel = Label(pcstdframe, text="% StdDev")
        self.StdDevLabel = Label(stdframe, text="StdDev")
        
        self.EqnLabel.pack(side=TOP)
        self.PcentStdDevLabel.pack(side=TOP)
        self.StdDevLabel.pack(side=TOP)
        
        self.Equations_Listbox_frame = eqnframe
        self.vsb = Scrollbar(stdframe, orient=VERTICAL)
        self.Equations_Listbox = Listbox(eqnframe, width="45", selectmode="extended", yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.OnVsb)
        #scrollbar.pack(side=RIGHT, fill=Y)
        self.Equations_Listbox.pack(side=TOP, fill=Y, expand=1)

        self.Equations_Listbox_frame.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        self.Equations_Listbox.bind("<ButtonRelease-1>", self.Equations_Listbox_Click)


        self.Pcentstddev_Listbox_frame = pcstdframe
        self.Pcentstddev_Listbox = Listbox(pcstdframe, width="15", selectmode="extended", yscrollcommand=self.vsb.set)
        self.Pcentstddev_Listbox.pack(side=TOP, fill=Y, expand=1)

        self.Pcentstddev_Listbox_frame.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        self.Pcentstddev_Listbox.bind("<ButtonRelease-1>", self.Pcentstddev_Listbox_Click)


        self.Stddev_Listbox_frame = stdframe
        self.Stddev_Listbox = Listbox(stdframe, width="15", selectmode="extended", yscrollcommand=self.vsb.set)
        self.vsb.pack(side=RIGHT, fill=Y, expand=1)
        self.Stddev_Listbox.pack(side=TOP, fill=Y, expand=1)

        self.Stddev_Listbox_frame.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        self.Stddev_Listbox.bind("<ButtonRelease-1>", self.Stddev_Listbox_Click)
        
        slab = Label(self.listframe,text="  "*200) # pin xframe and yframe to the left
        slab.pack(anchor=E, side=LEFT, expand=True,fill=BOTH)
        
        self.listframe.pack(anchor=NW, side=LEFT, fill=Y, expand=1)
        
        # place documentation text box
        self.doctextframe = Frame(self.bot_frame)
        
        yscrollbar = Scrollbar(self.doctextframe)
        yscrollbar.pack(side=RIGHT, fill=Y)
        
        self.doc_text = Text(self.doctextframe, width=80, height=6, yscrollcommand=yscrollbar.set)
        self.doc_text.pack(anchor=W, side=TOP, fill=BOTH, expand=1)
        self.doctextframe.pack(anchor=W, side=TOP, fill=BOTH, expand=1)
        yscrollbar.config(command=self.doc_text.yview)

        self.top_frame.pack(anchor=W, side=TOP, fill=BOTH, expand=1)
        self.bot_frame.pack(anchor=W, side=TOP, fill=BOTH, expand=1)


        self.Equations_Listbox.bind("<MouseWheel>", self.OnMouseWheel)
        self.Pcentstddev_Listbox.bind("<MouseWheel>", self.OnMouseWheel)
        self.Stddev_Listbox.bind("<MouseWheel>", self.OnMouseWheel)
        
        self.ShowHelp_Button_Click(None)

    def OnVsb(self, *args):
        self.Equations_Listbox.yview(*args)
        self.Pcentstddev_Listbox.yview(*args)
        self.Stddev_Listbox.yview(*args)

    def OnMouseWheel(self, event):
        self.Equations_Listbox.yview("scroll", event.delta,"units")
        self.Pcentstddev_Listbox.yview("scroll", event.delta,"units")
        self.Stddev_Listbox.yview("scroll", event.delta,"units")
        
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"
    
    def put_summaries_into_text_box(self):
        
        if len(self.selected_linfitL)>0:
            self.doc_text.delete(1.0, END)
            
            for n,i in enumerate(self.selected_linfitL):
                if n>0:
                    self.doc_text.insert(END, '\n'+'='*60+'\n')
                lf = self.guiObj.linear_fitL[i]
                print('Summary for... ',lf.get_eqn_str_w_consts())
                self.doc_text.insert(END, lf.get_full_description() )
                
        self.ShowHelpButton.configure(state=NORMAL,text="Show Help",width="18",relief=RAISED)
    
    def put_simple_fit_on_plot(self):
        
        XY = self.guiObj.XYjob
        
        curveL = []        
        if (XY.dataset and XY.dataset.N > 1) or len(self.selected_linfitL)>0:
            for n,i in enumerate(self.selected_linfitL):
                lf = self.guiObj.linear_fitL[i]
                curveL.append( lf )

            self.guiObj.PlotWin.make_new_plot(dataset=XY.dataset, curveL=curveL, 
                title_str='Simple Curve Fit')


    def Curvefit_Button_Click(self, event): 
        
        # clear the list boxes
        self.Equations_Listbox.delete(0, END)
        self.Pcentstddev_Listbox.delete(0, END)
        self.Stddev_Listbox.delete(0, END)
        
        # Also clear Exhaustive search results
        self.guiObj.pageD['Exhaustive Fit'].Equations_Listbox.delete(0, END)
        self.guiObj.pageD['Exhaustive Fit'].Pcentstddev_Listbox.delete(0, END)
        self.guiObj.pageD['Exhaustive Fit'].Stddev_Listbox.delete(0, END)
        
        
        XY = self.guiObj.XYjob
        max_terms = int( self.NTermsStringVar.get() )
        
        if "PcentStdDev" == self.RadioGroup1_StringVar.get():
            ordered_resultL = XY.fit_dataset_to_common_eqns(run_both=0, sort_by_pcent=1, max_terms=max_terms)
        else:
            ordered_resultL = XY.fit_dataset_to_common_eqns(run_both=0, sort_by_pcent=0, max_terms=max_terms)
            
        for lf in ordered_resultL:
            self.Equations_Listbox.insert(END, lf.get_eqn_str_w_consts())
            self.Pcentstddev_Listbox.insert(END, '%10.5f %%'%lf.pcent_std)
            self.Stddev_Listbox.insert(END, '%10g'%lf.std)
            
            #print lf.get_full_description()
            print('%-36s'%lf.get_eqn_str_w_consts(), '%10g'%lf.std, \
                '%10.5f'%lf.pcent_std, {0:'STD',1:'%std'}[lf.fit_best_pcent])
        print(ordered_resultL[0].get_full_description())
        
        self.guiObj.linear_fitL = ordered_resultL
        
        if ordered_resultL:
            self.Equations_Listbox.select_set(0)
            self.selected_linfitL = [0]
            self.put_simple_fit_on_plot()
            self.put_summaries_into_text_box()
            
            

    def Equations_Listbox_Click(self, event): 
        print('self.Equations_Listbox.curselection()=',self.Equations_Listbox.curselection())
        self.selected_linfitL = list(map(int, self.Equations_Listbox.curselection()))
        print('self.selected_linfitL=',self.selected_linfitL)
        self.put_summaries_into_text_box()
        self.put_simple_fit_on_plot()

    def Pcentstddev_Listbox_Click(self, event): #click method for component ID=3
        self.selected_linfitL = list(map(int, self.Pcentstddev_Listbox.curselection()))
        self.put_summaries_into_text_box()
        self.put_simple_fit_on_plot()

    def Stddev_Listbox_Click(self, event): #click method for component ID=2
        self.selected_linfitL = list(map(int, self.Stddev_Listbox.curselection()))
        self.put_summaries_into_text_box()
        self.put_simple_fit_on_plot()

    def RadioGroup1_StringVar_Callback(self, varName, index, mode):
        pass
        # >>>>>>insert any user code below this comment for section "RadioGroup1_StringVar_Callback"
        # replace, delete, or comment-out the following
        print("RadioGroup1_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.RadioGroup1_StringVar.get())

        
    def ShowHelp_Button_Click(self, event):
        #print 'Pressed ShowHelp Button'
        self.new_message('''The X,Y data can be fit to equations by minimizing either total error, or
percent error. Selecting the "Total Error" or "Percent Error" radio button
at upper left will determine which approach is used.

A limited set of common equations with 1 to 4 terms on the right hand side
is fit to the data when the "Curve Fit" button is pressed.

If fewer than 4 terms are desired, the "Max Terms" can be reduced from 4 
to the desired number.

All of the equations are listed in order from best to worst standard
deviation or percent standard deviation as appropriate.

Note that for some equations, divide by zero is allowed if it results in (1/infinity) which is equal to 0.0

The equations in "Simple Fit" are:

y = c0 + c1*x + c2*x**2 + c3*x**3 <-- CUBIC POLYNOMIAL
y = c0 + c1/x + c2*x + c3*x**2
y = c0 + c1/x + c2/x**2 + c3*x
y = c0 + c1/x + c2/x**2 + c3/x**3
y = c0 + c1*x + c2*x**2   <-- QUADRADIC POLYNOMIAL
y = c0 + c1*x + c2/x
y = c0 + c1/x + c2/x**2
y = 1/(c0 + c1/x + c2*x)
y = exp(c0 + c1*x + c2*log(x))
y = c0 + c1*x          <-- STRAIGHT LINE
y = c0 + c1/x
y = c0*x + c1*x**2     <-- QUADRADIC THROUGH ORIGIN
y = c0 + c1*log(x)
y = 1/(c0 + c1*x)      <-- STRAIGHT LINE FOR 1/y
y = 1/(c0 + c1/x)
y = 1/(c0 + c1*log(x))
y = 1/(c0*x + c1/x)
y = exp(c0 + c1*log(x))  <-- LINEARIZED EXPONENTIAL y=A*x**n
y = exp(c0 + c1/x)
y = exp(c0 + c1*x)
y = c0*x           <-- STRAIGHT LINE THROUGH ORIGIN
y = c0/x
y = c0   <-- MEAN OR WEIGHTED MEAN 
''')
        self.ShowHelpButton.configure(state=DISABLED,text="",width="1",relief=FLAT)
        
    
    def clear_messages(self):
        self.doc_text.delete(1.0, END)
        self.doc_text.update_idletasks()
        self.ShowHelpButton.configure(state=NORMAL,text="Show Help",width="18",relief=RAISED)
        
    def add_to_messages(self, s):
        self.doc_text.insert(END, s)
        self.doc_text.update_idletasks()
        self.ShowHelpButton.configure(state=NORMAL,text="Show Help",width="18",relief=RAISED)
        
    def new_message(self, s):
        self.clear_messages()
        self.doc_text.insert(END, s)
        self.doc_text.update_idletasks()
        self.ShowHelpButton.configure(state=NORMAL,text="Show Help",width="18",relief=RAISED)
        