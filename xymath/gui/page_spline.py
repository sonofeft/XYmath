from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object

from tkinter import *
from scipy.interpolate import UnivariateSpline
import os, sys
from xymath.splines import Spline

class SplinePage(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any issues.'''
        print('Leaving SplinePage')
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print('Entering SplinePage')
            
    def __init__(self, guiObj, pageFrame):
        
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
        
        # make frames
        self.main_frame = Frame(pageFrame)
        self.top_f = Frame(self.main_frame)
        self.top_left_f = Frame(self.top_f)
        self.top_right_f = Frame(self.top_f)
        
        self.selected_spline_nameL = []
        self.guiObj.selected_spline_objL = []
        self.selected_smoothing = 0.0

        self.Label_1 = Label(self.top_left_f,text="Select Spline(s)", width="15")
        self.Label_1.pack(anchor=NW, side=TOP)  #.place(x=36, y=6, width=200, height=22)


        lbframe = Frame( self.top_left_f )
        self.Listbox_1_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Listbox_1 = Listbox(lbframe, width="40", selectmode="extended", exportselection=0,
            yscrollcommand=scrollbar.set, height="7")
        scrollbar.config(command=self.Listbox_1.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Listbox_1.pack(side=LEFT, fill=BOTH, expand=1)

        self.Listbox_1_frame.pack(anchor=NW, side=TOP)  #.place(x=24, y=30, width=200, height=300)
        self.Listbox_1.bind("<ButtonRelease-1>", self.Listbox_1_Click)

        self.k_valueD = {} # holds polynomial order
        CONTROLS = [
            ("Linear Interpolation", 1),
            ("Quadratic Spline", 2),
            ("Cubic Spline", 3),
            ("Quartic Spline", 4),
            ("Quintic Spline", 5),
            ]
        for text, k in CONTROLS:
            self.Listbox_1.insert(END, text)
            self.k_valueD[text] = k
        
        # put smoothing control in place
        self.SmoothValLabel = Label(self.top_right_f, text="Smoothing (0=None)", justify=LEFT, anchor=W)
        self.SmoothValStringVar = StringVar(value="0")
        self.SmoothValSpinbox = Spinbox(self.top_right_f, from_=0, to=9, increment=0.1, textvariable=self.SmoothValStringVar)

        self.SmoothValStringVar_traceName = \
            self.SmoothValStringVar.trace_variable("w", self.SmoothValStringVar_Callback)

        self.SmoothValLabel2 = Label(self.top_right_f, text="Must Be >= 0.0", justify=LEFT, anchor=W)


        self.SmoothValLabel.pack(anchor=NW, side=TOP) #.place(x=240, y=30, width=160  )
        self.SmoothValSpinbox.pack(anchor=NW, side=TOP) #.place(x=240, y=60, width=100  )
        self.SmoothValLabel2.pack(anchor=NW, side=TOP)
        
        # ShowHelp Button
        self.ShowHelp_Button = Button(self.top_f,text="Show Help", width="15")
        self.ShowHelp_Button.bind("<ButtonRelease-1>", self.ShowHelp_Button_Click)

        
        # make text results area
        lbframe = Frame( self.main_frame )
        self.Messages_Text_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Messages_Text = Text(lbframe,  yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Messages_Text.yview)
        self.Messages_Text.pack(anchor=NW, side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=RIGHT, fill=Y)
        

        self.top_left_f.pack(anchor=NW, side=LEFT)
        self.top_right_f.pack(anchor=NW, side=LEFT, padx=18, pady=18)
        self.ShowHelp_Button.pack(anchor=SE, side=RIGHT)
        
        self.top_f.pack(anchor=NW, side=TOP, fill=X, expand=1)
        self.Messages_Text_frame.pack(anchor=NW, side=TOP, fill=BOTH, expand=1)

        self.main_frame.pack(anchor=NW, side=LEFT, fill=BOTH, expand=1)
        
        self.ShowHelp_Button_Click()


    def SmoothValStringVar_Callback(self, varName, index, mode):
        #print "SmoothValStringVar_Callback varName, index, mode",varName, index, mode
        #print "    new StringVar value =",self.SmoothValStringVar.get()
        self.put_splines_on_plot()
        
    def put_splines_on_plot(self):
        
        XY = self.guiObj.XYjob
        self.guiObj.selected_spline_objL = []
        
        try:
            self.selected_smoothing = float( self.SmoothValStringVar.get() )
        except:
            self.selected_smoothing = 0.0
        
        if self.selected_smoothing < 0.0:
            self.selected_smoothing = 0.0
        
        curveL = []
        descStr = '' # description string of spline(s)
        
        if (XY.dataset and XY.dataset.N > 1) or len(self.selected_spline_nameL)>0:
            for n,spline_name in enumerate(self.selected_spline_nameL):
                k = self.k_valueD[ spline_name ]
                
                if XY.dataset.N > 1 + k:
                    s = Spline( XY.dataset, order=k, smoothing=self.selected_smoothing)
                    self.guiObj.selected_spline_objL.append( s )
                    curveL.append( s )
                    if descStr:
                        descStr +=  '\n' + '='*44 + '\n'
                    descStr += s.get_full_description()
            
            if self.selected_smoothing==0:
                mytitle = 'Spline Interpolation'
            else:
                mytitle = 'Smoothed Spline Interpolation\n(StdDev=%g, %% StdDev=%g%%, CorrCoeff=%g)'%(s.std, s.pcent_std, s.corrcoef)
            
            self.guiObj.PlotWin.make_new_plot(dataset=XY.dataset, curveL=curveL, 
                title_str=mytitle)

        if descStr:
            self.new_message( descStr )                
            self.ShowHelp_Button.configure(state=NORMAL,text="Show Help",width="18",relief=RAISED)


    def ShowHelp_Button_Click(self, event=None): 
        #print 'Pressed ShowHelp Button'
        self.new_message('''Fit Spline Curve to Data.
        
1) Select the desired spline, or splines (order 1 to 5, Linear to Quintic)
2) Select any desired "smoothing"

If smoothing is equal to zero, the spline will go through all data points.

With smoothing added, the curve will go near the data points, but not necessarily through them. Click the Smoothing spin box to change the amount of smoothing.

Standard deviation and percent standard deviation will be calculated for smoothed splines along with their correlation coefficient.

Note that multiple splines can be fitted to the data simply by selecting more than one spline in the listbox.
''')
        self.ShowHelp_Button.configure(state=DISABLED,text="",width="1",relief=FLAT)


    
    def clear_messages(self):
        self.Messages_Text.delete(1.0, END)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show Help",width="15",relief=RAISED)
        
    def add_to_messages(self, s):
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show Help",width="15",relief=RAISED)
        
    def new_message(self, s):
        self.clear_messages()
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        self.ShowHelp_Button.configure(state=NORMAL,text="Show Help",width="15",relief=RAISED)


    def Listbox_1_Click(self, event): #click method for component ID=2
        #print "executed method Listbox_1_Click"
        #print "current selection(s) =",self.Listbox_1.curselection()
        self.selected_spline_nameL = []
        for i in self.Listbox_1.curselection():
            self.selected_spline_nameL.append( self.Listbox_1.get(i) )
            #self.selected_spline_nameL.append( self.k_valueD[self.Listbox_1.get(i)] )
        #print 'self.selected_spline_nameL =',self.selected_spline_nameL
        
        self.put_splines_on_plot()
    

