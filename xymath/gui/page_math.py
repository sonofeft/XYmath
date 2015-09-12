from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import os, sys
from tkinter import *
import numpy
from scipy import optimize

from xymath.math_funcs import find_min_max, find_root, find_integral, find_values_at_x
from xymath.helper_funcs import is_number
from xymath.dataset import DataSet
        
def floatCast( val=0.0 ):
    try:
        return float(val)
    except:
        return 0.0

class MathPage(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any issues.'''
        print('Leaving MathPage')
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print('Entering MathPage')
        XY = self.guiObj.XYjob
        
        if XY.dataset:
            self.Xmax_Entry_StringVar.set( str(XY.dataset.xmax) )
            self.Xmin_Entry_StringVar.set( str(XY.dataset.xmin) )
            
            # if Yval is already in range, leave it alone; otherwise set to average
            if is_number( self.At_Yval_Entry_StringVar.get() ):
                yval = floatCast( self.At_Yval_Entry_StringVar.get() )
                if yval<XY.dataset.yArr.min() or yval>XY.dataset.yArr.max():
                    self.At_Yval_Entry_StringVar.set('%g'%numpy.average( XY.dataset.yArr ) )
            else:
                self.At_Yval_Entry_StringVar.set('%g'%numpy.average( XY.dataset.yArr ) )
            
            # if X is already in range, leave it alone; otherwise set to average
            if is_number( self.At_X_Entry_StringVar.get() ):
                xval = floatCast( self.At_X_Entry_StringVar.get() )
                if xval<XY.dataset.xmin or xval>XY.dataset.xmax:
                    self.At_X_Entry_StringVar.set('%g'%numpy.average( XY.dataset.xArr ) )
            else:
                self.At_X_Entry_StringVar.set('%g'%numpy.average( XY.dataset.xArr ) )
            
        else:
            self.Xmax_Entry_StringVar.set( '10' )
            self.Xmin_Entry_StringVar.set( '0' )
            self.At_Yval_Entry_StringVar.set('5')
            self.At_X_Entry_StringVar.set('5')
            
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
        
        self.select_f = Frame(self.main_frame)
        self.right_f = Frame(self.main_frame)
        
        self.far_right_f = Frame(self.right_f)
        self.range_f = Frame(self.right_f)
        self.min_f = Frame(self.right_f)
        self.root_f = Frame(self.right_f)
        self.eval_f = Frame(self.right_f)
        self.error_f = Frame(self.right_f)

        
        # ShowHelp Button
        self.ShowHelp_Button = Button(self.far_right_f,text="Show Help", width="15")
        self.ShowHelp_Button.bind("<ButtonRelease-1>", self.ShowHelp_Button_Click)

        # make buttons
        self.Error_Button = Button(self.error_f,text="Show Error", width="25")
        self.Error_Button.pack(anchor=NW, side=LEFT)
        self.Error_Button.bind("<ButtonRelease-1>", self.Error_Button_Click)
        self.PcentError_Button = Button(self.error_f,text="Show Percent Error", width="25")
        self.PcentError_Button.pack(anchor=NW, side=LEFT)
        self.PcentError_Button.bind("<ButtonRelease-1>", self.PcentError_Button_Click)
        
        self.Evaluate_Button = Button(self.eval_f,text="Evaluate Y & dY/dX at X=", width="25")
        self.Evaluate_Button.pack(anchor=NW, side=LEFT)
        self.Evaluate_Button.bind("<ButtonRelease-1>", self.Evaluate_Button_Click)
        self.Eq1_Label = Label(self.eval_f,text=" X=", width="3")
        self.Eq1_Label.pack(anchor=NW, side=LEFT)

        self.Findminmax_Button = Button(self.min_f,text="Find Min/Max", width="25")
        self.Findminmax_Button.pack(anchor=NW, side=TOP)
        self.Findminmax_Button.bind("<ButtonRelease-1>", self.Findminmax_Button_Click)

        self.Findroot_Button = Button(self.root_f,text="Find X Root at Y=", width="25")
        self.Findroot_Button.pack(anchor=NW, side=LEFT)
        self.Findroot_Button.bind("<ButtonRelease-1>", self.Findroot_Button_Click)
        self.Eq_Label = Label(self.root_f,text=" Y=", width="3")
        self.Eq_Label.pack(anchor=NW, side=LEFT)

        self.Integrate_Button = Button(self.min_f,text="Integrate Curve", width="25")
        self.Integrate_Button.pack(anchor=NW, side=TOP)
        self.Integrate_Button.bind("<ButtonRelease-1>", self.Integrate_Button_Click)
        
        self.At_X_Entry = Entry(self.eval_f,width="12")
        self.At_X_Entry.pack(anchor=NW, side=LEFT)
        self.At_X_Entry_StringVar = StringVar()
        self.At_X_Entry.configure(textvariable=self.At_X_Entry_StringVar)
        self.At_X_Entry_StringVar.set("Xval")
        self.At_X_Entry_StringVar_traceName = self.At_X_Entry_StringVar.trace_variable("w", self.At_X_Entry_StringVar_Callback)

        self.At_Yval_Entry = Entry(self.root_f,width="12")
        self.At_Yval_Entry.pack(anchor=NW, side=LEFT)
        self.At_Yval_Entry_StringVar = StringVar()
        self.At_Yval_Entry.configure(textvariable=self.At_Yval_Entry_StringVar)
        self.At_Yval_Entry_StringVar.set("Yval")
        self.At_Yval_Entry_StringVar_traceName = self.At_Yval_Entry_StringVar.trace_variable("w", self.At_Yval_Entry_StringVar_Callback)


        self.Select_Label = Label(self.select_f,text="Select Curve", width="15")
        self.Select_Label.pack(anchor=NW, side=TOP)


        self.Xrange_Label = Label(self.range_f,text="X Range = ", width="12")
        self.Xrange_Label.pack(anchor=NW, side=LEFT)

        self.Xmin_Entry = Entry(self.range_f,width="12")
        self.Xmin_Entry.pack(anchor=NW, side=LEFT)
        self.Xmin_Entry_StringVar = StringVar()
        self.Xmin_Entry.configure(textvariable=self.Xmin_Entry_StringVar)
        self.Xmin_Entry_StringVar.set("Xmin")
        self.Xmin_Entry_StringVar_traceName = self.Xmin_Entry_StringVar.trace_variable("w", self.Xmin_Entry_StringVar_Callback)

        self.To_Label = Label(self.range_f,text="to", justify="center", width="7")
        self.To_Label.pack(anchor=NW, side=LEFT)

        self.Xmax_Entry = Entry(self.range_f,width="12")
        self.Xmax_Entry.pack(anchor=NW, side=LEFT)
        self.Xmax_Entry_StringVar = StringVar()
        self.Xmax_Entry.configure(textvariable=self.Xmax_Entry_StringVar)
        self.Xmax_Entry_StringVar.set("Xmax")
        self.Xmax_Entry_StringVar_traceName = self.Xmax_Entry_StringVar.trace_variable("w", self.Xmax_Entry_StringVar_Callback)

        
        # make text results area
        lbframe = Frame( self.right_f )
        self.Messages_Text_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Messages_Text = Text(lbframe, width="45", height="12", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Messages_Text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Messages_Text.pack(side=LEFT, fill=BOTH, expand=1)



        lbframe = Frame( self.select_f )
        self.Listbox_1_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Listbox_1 = Listbox(lbframe, width="35", height='20', exportselection=0,
            selectmode="normal", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Listbox_1.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Listbox_1.pack(side=LEFT, fill=BOTH, expand=1)

        self.Listbox_1_frame.pack(anchor=NW, side=TOP, expand=True,fill=Y)
        self.Listbox_1.bind("<ButtonRelease-1>", self.Listbox_1_Click)
        
        self.range_f.pack(anchor=NW, side=TOP)
        self.min_f.pack(anchor=NW, side=TOP)
        self.root_f.pack(anchor=NW, side=TOP)
        self.eval_f.pack(anchor=NW, side=TOP)
        self.error_f.pack(anchor=NW, side=TOP)
        
        self.select_f.pack(anchor=NW, side=LEFT, expand=True,fill=Y)
        
        slab = Label(self.far_right_f,text=" ") # pin xframe and yframe to the left
        slab.pack(anchor=E, side=LEFT, expand=True,fill=BOTH)
        self.ShowHelp_Button.pack(anchor=NE, side=TOP)
        self.far_right_f.pack(anchor=E, side=TOP)
        self.Messages_Text_frame.pack(anchor=NW, side=TOP, fill=BOTH, expand=1)
        
        self.right_f.pack(anchor=W, side=LEFT, expand=True,fill=BOTH)
        
        self.main_frame.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.ShowHelp_Button_Click()


    def ShowHelp_Button_Click(self, event=None): 
        #print 'Pressed ShowHelp Button'
        self.new_message('''All math operations are limited to the X Range selected above.

Select the equation of interest in the list box. Equations are generated in "Simple Fit", "Spline", "Exhaustive Fit" and "Non-Linear Fit".

"Find Min/Max" will find the minimum and maximum y values in the X Range.

"Integrate Curve" will perform a numerical integration over the X Range.

"Find X Root at Y" will discover what value or values of x result in the desired value of y.

"Evaluate Y & dY/dX at X" will calculate the value of y as well as 1st and 2nd derivatives at the desired value of x.
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

    def Listbox_1_Click(self, event):
        #print "executed method Listbox_1_Click"
        #print "current selection(s) =",self.Listbox_1.curselection()
        #labelL = []
        #for i in self.Listbox_1.curselection():
        #    labelL.append( self.Listbox_1.get(i))
        #print "current label(s) =",labelL
        self.special_title = 'Math Functions' # for putting annotations on plot
        self.put_equation_on_plot()

    def At_X_Entry_StringVar_Callback(self, varName, index, mode):
        print("At_X_Entry_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.At_X_Entry_StringVar.get())


    def At_Yval_Entry_StringVar_Callback(self, varName, index, mode):
        print("At_Yval_Entry_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.At_Yval_Entry_StringVar.get())


    def Xmax_Entry_StringVar_Callback(self, varName, index, mode):
        print("Xmax_Entry_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.Xmax_Entry_StringVar.get())


    def Xmin_Entry_StringVar_Callback(self, varName, index, mode):
        print("Xmin_Entry_StringVar_Callback varName, index, mode",varName, index, mode)
        print("    new StringVar value =",self.Xmin_Entry_StringVar.get())
    
    def put_equation_on_plot(self, integFill=None):
        
        if len(self.Listbox_1.curselection()):
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]
            
            XY = self.guiObj.XYjob
            
            if hasattr(self, 'xlo'):
                ylo = obj.eval_xrange( self.xlo )
                yhi = obj.eval_xrange( self.xhi )
                range_tuple = ([self.xlo, self.xhi], [ylo,yhi], '|', 25, 'X Range=%g to %g'%(self.xlo, self.xhi))
                if type(self.specialPtL) == type([]):
                    self.specialPtL.append( range_tuple )
                else:
                    self.specialPtL= [range_tuple]
            
            curveL = [obj]
            self.guiObj.PlotWin.make_new_plot(dataset=XY.dataset, curveL=curveL, 
                title_str=self.special_title, integFill=integFill, specialPtL=self.specialPtL)


    def evaluate_float_entries(self):
        self.xlo = floatCast( self.Xmin_Entry_StringVar.get() )
        self.xhi = floatCast( self.Xmax_Entry_StringVar.get() )
        self.yval = floatCast( self.At_Yval_Entry_StringVar.get() )
        self.xval = floatCast( self.At_X_Entry_StringVar.get() )
        self.special_title = 'Math Functions' # for putting annotations on plot
        self.specialPtL = None

    def Evaluate_Button_Click(self, event):
        self.evaluate_float_entries()
        if len(self.Listbox_1.curselection()):
            self.new_message('Evaluate Value and Derivatives\n')
            
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]
            
            resultL = find_values_at_x(obj, self.xval, xlo=self.xlo, xhi=self.xhi)
            
            dx = old_div((self.xhi-self.xlo), 1000.0)
            s = 'of %s \nusing range x=%g to %g for dx=%g\n'%(str(self.equationL[i].name),self.xlo, self.xhi, dx)
            self.add_to_messages( s )
            
            s = '\nat X=%g \n'%(self.xval,)
            self.add_to_messages( s )
            stL = [s.strip().title()]
            
            s = '\nY=%g \n'%(resultL[0])
            self.add_to_messages( s )
            stL.append( s.strip() )
            
            s = '\ndY/dX=%g \n'%(resultL[1])
            self.add_to_messages( s )
            stL.append( '\n'+ s.strip().lower() )
            
            s = '\nd2Y/dX2=%g \n'%(resultL[2])
            self.add_to_messages( s )
            stL.append( s.strip().lower() )
            
            self.special_title =  ', '.join(stL)
            self.specialPtL = [([self.xval], [resultL[0]], 'D', 15, '(%g, %g)'%(self.xval, resultL[0]))]
            
            self.put_equation_on_plot()
        else:
            self.new_message('No Selection for Evaluation.\n')

    def Findminmax_Button_Click(self, event):
        self.evaluate_float_entries()
        if len(self.Listbox_1.curselection()):
            self.new_message('Finding Minimum and Maximum Y Values\n')
            
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]
            
            x_min, y_min, x_max, y_max = \
                find_min_max(obj, xlo=self.xlo, xhi=self.xhi, xtol=1.0e-12)
        
            s = 'of %s \nover range x=%g to %g\n'%(str(self.equationL[i].name),self.xlo, self.xhi)
            self.add_to_messages( s )
            
            s = '\nYminimum=%g at X=%g\n'%(y_min, x_min)
            self.add_to_messages( s )
            #stL = [s.strip()]
            s = '\nYmaximum=%g at X=%g\n'%(y_max, x_max)
            #stL.append( s.strip() )
            
            self.special_title =  'Min/Max of ' + obj.name
            self.add_to_messages( s )
            
            self.specialPtL = [([x_max], [y_max], '^', 15, 'Max (%g, %g)'%(x_max, y_max)) ]
            self.specialPtL.append( ([x_min], [y_min], 'v', 15, 'Min (%g, %g)'%(x_min, y_min)) )
            
            self.put_equation_on_plot()
        else:
            self.new_message('No Selection for Min/Max Calculation.\n')
        

    def Findroot_Button_Click(self, event):
        self.evaluate_float_entries()
        if len(self.Listbox_1.curselection()):
            self.new_message('Finding Root X for Y=%g\n'%self.yval)
            
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]
            
            xRootArr, yRootArr = find_root(obj, ygoal=self.yval, xlo=self.xlo, xhi=self.xhi)
        
            s = 'of %s \nover range x=%g to %g\n'%(str(self.equationL[i].name),self.xlo, self.xhi)
            self.add_to_messages( s )
            
            NRoots = len(xRootArr)
            if NRoots==1:
                s = '\nThere is one Root\n'
            else:
                s = '\nThere are %i Roots\n'%(NRoots,)
            self.add_to_messages( s )
            self.special_title =  s.strip() + ' for Y=%g'%self.yval
            #stL = [s.strip()]
            
            self.specialPtL = []
            for i in range(NRoots):
                s = '\nYroot=%g at X=%g\n'%(yRootArr[i], xRootArr[i])
                #stL.append( s.strip() )
                self.add_to_messages( s )
                self.specialPtL.append( ([xRootArr[i]], [yRootArr[i]], '*', 20, '(%g, %g)'%(xRootArr[i], yRootArr[i])) )
            
            #self.special_title =  ', '.join(stL)
            self.put_equation_on_plot()
        else:
            self.new_message('No Selection for Root Finding Calculation.\n')

    def Integrate_Button_Click(self, event):
        self.evaluate_float_entries()
        if len(self.Listbox_1.curselection()):
            self.new_message('Finding Integral\n')
            
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]
            
            integral, error = find_integral(obj, xlo=self.xlo, xhi=self.xhi)
        
            s = 'of %s \nover range x=%g to %g\n'%(str(self.equationL[i].name),self.xlo, self.xhi)
            self.add_to_messages( s )
            
            s = '\nIntegral=%g (Area Under Curve)\n'%(integral,)
            self.add_to_messages( s )
            stL = ['Integral=%g '%(integral,)]
            s = '\n     +/- %g error\n'%(error,)
            self.add_to_messages( s )
            
            stL.append( s.strip() )
            stL.append( '\nover range x=%g to %g\n'%(self.xlo, self.xhi) )
            
            self.special_title =  ', '.join(stL)
            
            xPlotArr, yPlotArr = obj.get_xy_plot_arrays( Npoints=100, logScale=0, xmin=self.xlo, xmax=self.xhi)
            self.put_equation_on_plot(integFill=(xPlotArr, yPlotArr))
        else:
            self.new_message('No Selection for Integration.\n')


    def Error_Button_Click(self, event):
        self.evaluate_float_entries()
        if len(self.Listbox_1.curselection()):
            self.new_message('Showing Error of:\n')
            
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]

            self.add_to_messages( obj.get_full_description() )

            XY = self.guiObj.XYjob
        
            if XY.dataset:
                
                yeqnArr = obj.eval_xrange( XY.dataset.xArr )
                errArr = XY.dataset.yArr - yeqnArr
                errDS = DataSet( XY.dataset.xArr, errArr, xName=XY.dataset.xName, 
                                 yName=XY.dataset.yName+ ' (data - eqn)',
                                 xUnits=XY.dataset.xUnits, yUnits=XY.dataset.yUnits )
                
                xArr = [XY.dataset.xmin, XY.dataset.xmax]
                yArr = [ obj.std,  obj.std]
                textLabelCurveL = [(xArr, yArr, 'red', 1, '--', '1 StdDev')]
                textLabelCurveL.append((xArr, [ -obj.std,  -obj.std], 'red', 1, '--', ''))
                textLabelCurveL.append((xArr, [ 0., 0.], 'red', 1, '-', ''))
                
                self.guiObj.PlotWin.make_new_plot(dataset=errDS, textLabelCurveL=textLabelCurveL, 
                    title_str=XY.dataset.yName+' Error\n in eqn: '+str(self.equationL[i].name),  
                    specialPtL=None, dataLabel='Error', force_linear_y=True)
            
        else:
            self.new_message('No Selection for Error.\n')

    def PcentError_Button_Click(self, event):
        self.evaluate_float_entries()
        if len(self.Listbox_1.curselection()):
            self.new_message('Showing Percent Error of:\n')
            
            i = int(self.Listbox_1.curselection()[0])
            obj = self.equationL[i]

            self.add_to_messages( obj.get_full_description() )

            XY = self.guiObj.XYjob
        
            if XY.dataset:
                
                yeqnArr = obj.eval_xrange( XY.dataset.xArr )
                pcerrArr = -100.0 * (yeqnArr - XY.dataset.yArr) / numpy.absolute( XY.dataset.yArr )
                
                errDS = DataSet( XY.dataset.xArr, pcerrArr, xName=XY.dataset.xName, 
                                 yName=XY.dataset.yName+ ' [100*(data - eqn)/data]',
                                 xUnits=XY.dataset.xUnits, yUnits=XY.dataset.yUnits )
                
                xArr = [XY.dataset.xmin, XY.dataset.xmax]
                yArr = [ obj.pcent_std,  obj.pcent_std]
                textLabelCurveL = [(xArr, yArr, 'red', 1, '--', '1 PcntStdDev')]
                textLabelCurveL.append((xArr, [ -obj.pcent_std,  -obj.pcent_std], 'red', 1, '--', ''))
                textLabelCurveL.append((xArr, [ 0., 0.], 'red', 1, '-', ''))
                
                self.guiObj.PlotWin.make_new_plot(dataset=errDS, textLabelCurveL=textLabelCurveL, 
                    title_str=XY.dataset.yName+' Percent Error\n in eqn: '+str(self.equationL[i].name),  
                    specialPtL=None, dataLabel='Percent Error', force_linear_y=True)
            
        else:
            self.new_message('No Selection for Percent  Error.\n')
