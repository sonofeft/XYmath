from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import map
from builtins import object
import os, sys
from math import factorial
from tkinter import *
from xymath.exhaustive import full_funcL, full_xtranL, full_ytranL, build_xterms, num_combinations

class ExhaustPage(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any XYjob issues.'''
        print('Leaving ExhaustPage')
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print('Entering ExhaustPage')

    #def __init__(self, master, pageFrame):
    def __init__(self, guiObj, pageFrame):
        
        self.num_search_eqns = 0 # possible combinations to be searched
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
        
        self.selected_linfitL = []
        
        # build check boxes for selecting functions
        self.very_top1 = Frame(pageFrame, pady=0)
        self.FunctionChoice = Label(self.very_top1, text="Function Terms", width=12)
        self.FunctionChoice.pack(anchor=NW, side=LEFT)
        
        self.funcVarL = []
        for i,f in enumerate(full_funcL):
            var = IntVar()
            self.funcVarL.append( var )
            if i<3:
                var.set(1)
            else:
                var.set(0)
            cb = Checkbutton(self.very_top1, text=f, variable=var, pady=0, borderwidth=0,
                command=self.Checkbutton_IntVar_Callback)
            cb.pack(anchor=NW, side=LEFT)
            
        # Next row of selections, x transforms
        self.very_top2 = Frame(pageFrame, pady=0)
        self.XTransformChoice = Label(self.very_top2, text="X Transforms", width=12)
        self.XTransformChoice.pack(anchor=NW, side=LEFT)
        
        self.xtransVarL = []
        for i,f in enumerate(full_xtranL):
            var = IntVar()
            self.xtransVarL.append( var )
            if i<3:
                var.set(1)
            else:
                var.set(0)
            cb = Checkbutton(self.very_top2, text=f, variable=var, pady=0, borderwidth=0,
                command=self.Checkbutton_IntVar_Callback)
            cb.pack(anchor=NW, side=LEFT)
            
        # Next row of selections, y transforms
        self.very_top3 = Frame(pageFrame, pady=0)
        self.YTransformChoice = Label(self.very_top3, text="Y Transforms", width=12)
        self.YTransformChoice.pack(anchor=NW, side=LEFT)
        
        self.ytransVarL = []
        for i,f in enumerate(full_ytranL):
            var = IntVar()
            self.ytransVarL.append( var )
            if i<3:
                var.set(1)
            else:
                var.set(0)
            cb = Checkbutton(self.very_top3, text=f, variable=var, pady=0, borderwidth=0,
                command=self.Checkbutton_IntVar_Callback)
            cb.pack(anchor=NW, side=LEFT)
            
            
            
        # Put in the rest of the stuff after y transforms        
        self.top_frame = Frame(pageFrame)
        self.bot_frame = Frame(pageFrame)
        
        self.listframe = Frame(self.top_frame)
        self.choiceframe = Frame(self.top_frame)
        
        # set up choiceframe
        self.Curvefit_Button = Button(self.choiceframe,text="Curve Fit", width="18", height="2", bg='#ccffcc')
        self.Curvefit_Button.bind("<ButtonRelease-1>", self.Curvefit_Button_Click)

        self.Fitby_Labelframe = LabelFrame(self.choiceframe,text="Fit By:", height="132", width="189")

        self.Pcenterror_Radiobutton = Radiobutton(self.Fitby_Labelframe,text="Percent Error", 
            value="PcentStdDev", width="15", anchor=W)
        self.Pcenterror_Radiobutton.pack(anchor=NW, side=TOP)
        self.RadioGroup1_StringVar = StringVar()
        self.RadioGroup1_StringVar.set("PcentStdDev")
        self.RadioGroup1_StringVar_traceName = self.RadioGroup1_StringVar.trace_variable("w", self.RadioGroup1_StringVar_Callback)
        self.Pcenterror_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

        self.Total_Radiobutton = Radiobutton(self.Fitby_Labelframe,text="Total Error", 
            value="StdDev", width="15", anchor=W)
        self.Total_Radiobutton.pack(anchor=NW, side=TOP)
        self.Total_Radiobutton.configure(variable=self.RadioGroup1_StringVar )
        
        # Number of terms Spinbox
        self.NTermsLabel = Label(self.choiceframe, text="Number of Terms")
        self.NTermsStringVar = StringVar(value="3")
        self.NtermsSpinbox = Spinbox(self.choiceframe, from_=1, to=9, textvariable=self.NTermsStringVar)
        self.NTermsStringVar_traceName = self.NTermsStringVar.trace_variable("w", self.NTermsStringVar_Callback)


        self.NSavedEqnsLabel_space = Label(self.choiceframe, text=" ")
        self.NSavedEqnsLabel = Label(self.choiceframe, text="Saved Equations")
        self.NSavedEqnsStringVar = StringVar(value="100")
        self.max_saved_eqns = 100
        self.NSavedEqnsSpinbox = Spinbox(self.choiceframe, from_=10, to=10000, increment=50, textvariable=self.NSavedEqnsStringVar)
        self.NSavedEqnsStringVar_traceName = self.NSavedEqnsStringVar.trace_variable("w", self.NSavedEqnsStringVar_Callback)

        
        self.Btn_Space = Label(self.choiceframe,text=" ")
        
        self.ShowHelpButton = Button(self.choiceframe,text="Show Help", width="18")
        self.ShowHelpButton.bind("<ButtonRelease-1>", self.ShowHelp_Button_Click)
        

        self.Fitby_Labelframe.pack(anchor=NW, side=TOP)
        self.Curvefit_Button.pack(anchor=NW, side=TOP)
        
        self.NTermsLabel.pack(anchor=NW, side=TOP)
        self.NtermsSpinbox.pack(anchor=NW, side=TOP)
        
        self.NSavedEqnsLabel_space.pack(anchor=NW, side=TOP)
        self.NSavedEqnsLabel.pack(anchor=NW, side=TOP)
        self.NSavedEqnsSpinbox.pack(anchor=NW, side=TOP)

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

        self.very_top1.pack(anchor=W, side=TOP, fill=X, expand=0)
        self.very_top2.pack(anchor=W, side=TOP, fill=X, expand=0)
        self.very_top3.pack(anchor=W, side=TOP, fill=X, expand=0)
        self.top_frame.pack(anchor=W, side=TOP, fill=BOTH, expand=1)
        self.bot_frame.pack(anchor=W, side=TOP, fill=BOTH, expand=1)


        self.Equations_Listbox.bind("<MouseWheel>", self.OnMouseWheel)
        self.Pcentstddev_Listbox.bind("<MouseWheel>", self.OnMouseWheel)
        self.Stddev_Listbox.bind("<MouseWheel>", self.OnMouseWheel)

        self.calc_number_of_search_eqns()
        
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
    
    def put_curve_fit_on_plot(self):
        
        XY = self.guiObj.XYjob        
        
        curveL = []        
        if (XY.dataset and XY.dataset.N > 1) or len(self.selected_linfitL)>0:
            for n,i in enumerate(self.selected_linfitL):
                lf = self.guiObj.linear_fitL[i]
                curveL.append( lf )

            self.guiObj.PlotWin.make_new_plot(dataset=XY.dataset, curveL=curveL, 
                title_str='Exhaustive Curve Fit')


    def Curvefit_Button_Click(self, event): 
        
        # clear the list boxes
        self.Equations_Listbox.delete(0, END)
        self.Pcentstddev_Listbox.delete(0, END)
        self.Stddev_Listbox.delete(0, END)
        self.guiObj.linear_fitL = []

        
        # Also clear Simple search results
        self.guiObj.pageD['Simple Fit'].Equations_Listbox.delete(0, END)
        self.guiObj.pageD['Simple Fit'].Pcentstddev_Listbox.delete(0, END)
        self.guiObj.pageD['Simple Fit'].Stddev_Listbox.delete(0, END)


        XY = self.guiObj.XYjob
        num_terms = int( self.NTermsStringVar.get() )
        self.calc_possibel_terms_in_eqn() # calcs self.funcL and self.xtranL
        
        # build list of y transforms
        ytranL = []        
        for s,var in zip(full_ytranL, self.ytransVarL):
            if int(var.get()):
                ytranL.append(s)
        
        if "PcentStdDev" == self.RadioGroup1_StringVar.get():
            run_best_pcent = 1
        else:
            run_best_pcent = 0
        
        # === Iterate over exhaustive fit
        for ifit, linfit in enumerate(XY.fit_dataset_to_exhaustive_search( run_best_pcent=run_best_pcent, 
                                    num_terms=num_terms, funcL=self.funcL, xtranL=self.xtranL,  ytranL=ytranL)):
            
            if linfit.is_good_over_plot_range(): # std==INFINITY is caught in XYjob
                self.guiObj.linear_fitL.append( linfit )
            
            if (ifit+1) % 10 == 0:
                self.Curvefit_Button.configure(text='Fit %g of %g\nEquations'%(ifit+1, self.num_search_eqns) )
                self.Curvefit_Button.update_idletasks()
                self.choiceframe.update_idletasks()
            
            if (ifit+1) % 50 == 0:
                self.show_current_results(run_best_pcent)
                self.Equations_Listbox.update_idletasks()
                self.Pcentstddev_Listbox.update_idletasks()
                self.Stddev_Listbox.update_idletasks()
                self.guiObj.PlotWin.update_idletasks()
                self.pageFrame.update_idletasks()
            
            #print ifit+1,'Equations'
            
        self.show_current_results(run_best_pcent)
        self.Curvefit_Button.configure(text='Curve Fit\n%g Equations'%self.num_search_eqns)
        
    def show_current_results(self, run_best_pcent):
        if run_best_pcent:
            self.guiObj.linear_fitL.sort( key=lambda lf: lf.pcent_std)
        else:
            self.guiObj.linear_fitL.sort( key=lambda lf: lf.std)
                
        if len( self.guiObj.linear_fitL ) > self.max_saved_eqns:
            self.guiObj.linear_fitL = self.guiObj.linear_fitL[:self.max_saved_eqns]
        
        self.Equations_Listbox.delete(0, END)
        self.Pcentstddev_Listbox.delete(0, END)
        self.Stddev_Listbox.delete(0, END)
    
            
        for lf in self.guiObj.linear_fitL:
            self.Equations_Listbox.insert(END, lf.get_eqn_str_w_consts())
            self.Pcentstddev_Listbox.insert(END, '%10.5f %%'%lf.pcent_std)
            self.Stddev_Listbox.insert(END, '%10g'%lf.std)
            
            #print lf.get_full_description()
            #print  '%-36s'%lf.get_eqn_str_w_consts(), '%10g'%lf.std, \
            #    '%10.5f'%lf.pcent_std, {0:'STD',1:'%std'}[lf.fit_best_pcent]
        print(self.guiObj.linear_fitL[0].get_full_description())
        
        
        if self.guiObj.linear_fitL:
            self.Equations_Listbox.select_set(0)
            self.selected_linfitL = [0]
            self.put_curve_fit_on_plot()
            self.put_summaries_into_text_box()
            

    def Equations_Listbox_Click(self, event): 
        print('self.Equations_Listbox.curselection()=',self.Equations_Listbox.curselection())
        self.selected_linfitL = list(map(int, self.Equations_Listbox.curselection()))
        print('self.selected_linfitL=',self.selected_linfitL)
        self.put_summaries_into_text_box()
        self.put_curve_fit_on_plot()

    def Pcentstddev_Listbox_Click(self, event): #click method for component ID=3
        self.selected_linfitL = list(map(int, self.Pcentstddev_Listbox.curselection()))
        self.put_summaries_into_text_box()
        self.put_curve_fit_on_plot()

    def Stddev_Listbox_Click(self, event): #click method for component ID=2
        self.selected_linfitL = list(map(int, self.Stddev_Listbox.curselection()))
        self.put_summaries_into_text_box()
        self.put_curve_fit_on_plot()

    def RadioGroup1_StringVar_Callback(self, varName, index, mode):
        pass
        # >>>>>>insert any user code below this comment for section "RadioGroup1_StringVar_Callback"
        # replace, delete, or comment-out the following
        print("RadioGroup1_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.RadioGroup1_StringVar.get())

    def NSavedEqnsStringVar_Callback(self, varName, index, mode):
        pass
        # >>>>>>insert any user code below this comment for section "NSavedEqnsStringVar_Callback"
        # replace, delete, or comment-out the following
        print("NSavedEqnsStringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.NSavedEqnsStringVar.get())
        try:
            max_saved_eqns = int( self.NSavedEqnsStringVar.get() )
            self.max_saved_eqns = max_saved_eqns
        except:
            print('Error in spinbox for Saved Equations',self.NSavedEqnsStringVar.get(),'!= integer')

    def NTermsStringVar_Callback(self, varName, index, mode):
        pass
        # >>>>>>insert any user code below this comment for section "NTermsStringVar_Callback"
        # replace, delete, or comment-out the following
        print("NTermsStringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.NTermsStringVar.get())
        self.calc_number_of_search_eqns()

    def calc_possibel_terms_in_eqn(self):
        self.funcL=[]
        self.xtranL=[]
        
        for s,var in zip(full_funcL, self.funcVarL):
            if int(var.get()):
                self.funcL.append(s)
        
        for s,var in zip(full_xtranL, self.xtransVarL):
            if int(var.get()):
                self.xtranL.append(s)
        
        self.termL = build_xterms(funcL=self.funcL, xtranL=self.xtranL)

    def calc_number_of_search_eqns(self):
        self.calc_possibel_terms_in_eqn()
        ny = 0
        for var in self.ytransVarL:
            if int(var.get()):
                ny += 1
        num_terms = int( self.NTermsStringVar.get() )        
        self.num_search_eqns = num_combinations(self.termL, num_terms) * ny
        self.Curvefit_Button.configure(text='Curve Fit\n%g Equations'%self.num_search_eqns)


    def Checkbutton_IntVar_Callback(self):
        print("Checkbutton_StringVar_Callback")
        self.calc_number_of_search_eqns()
        
        
    def ShowHelp_Button_Click(self, event):
        #print 'Pressed ShowHelp Button'
        self.new_message('''The X,Y data can be fit to equations by minimizing either total error, or
percent error. Selecting the "Total Error" or "Percent Error" radio button
will determine which approach is used.

Equations are generated by using all linear combinations of terms and
transforms selected. Each equation has the number of terms selected.

Selecting function terms of "const", "x" and "x**2" results in all
combinations of those terms on the right hand side of the equations.
Each of those x terms can be modified by x transforms.

Selecting x transforms of "x", "1/x" and "log(x)" results in all terms
using x being transformed into "x", "1/x" or "log(x)". For example
"x**2" would become "x**2", "1/x**2" or "log(x)**2".

Selecting y transforms of "y", "1/y" and "y**2" results in y=f(x),
1/y=f(x) and y**2=f(x) all being examined.

All of the equations are listed in order from best to worst standard
deviation or percent standard deviation as appropriate.

By default, only the top 100 equations are listed, however, that can
be changed with the "Saved Equations" selection box.

Note that for some equations, divide by zero is allowed if it results in (1/infinity) which is equal to 0.0
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
                