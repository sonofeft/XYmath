from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object

from tkinter import *
import tkinter.font
from xymath.gui.dropdown import Dropdown

class PagePlot(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any issues.'''
        print('Leaving PagePlot')
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        print('Entering PagePlot')
            
    def __init__(self, guiObj, pageFrame):
        
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
        
        self.plotOptionD = {} # holds all plot options

        self.a_frame = LabelFrame(pageFrame, text="Plot")
        self.b_frame = LabelFrame(pageFrame, text="Equations")
        self.cc_frame = Frame(pageFrame)
        self.c_frame = LabelFrame(self.cc_frame, text="Data Points")

        # A Frame =======================================================================
        # X Axis linear/log choice
        self.XAxis_Labelframe = LabelFrame(self.a_frame,text="X Axis:")

        self.XAxis_Linear_Radiobutton = Radiobutton(self.XAxis_Labelframe,text="Linear", 
            value="Linear", width="15", anchor=W)
        self.XAxis_Linear_Radiobutton.pack(anchor=NW, side=TOP)
        self.RadioGroup1_StringVar = StringVar()
        self.RadioGroup1_StringVar.set("Linear")
        self.RadioGroup1_StringVar_traceName = self.RadioGroup1_StringVar.trace_variable("w", self.RadioGroup1_StringVar_Callback)
        self.XAxis_Linear_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

        self.XAxis_Log_Radiobutton = Radiobutton(self.XAxis_Labelframe,text="Log", 
            value="Log", width="15", anchor=W)
        self.XAxis_Log_Radiobutton.pack(anchor=NW, side=TOP)
        self.XAxis_Log_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

        # Show X Minor Log Ticks
        self.XMinorTicks_CB = Checkbutton(self.XAxis_Labelframe,text="Show logX Minor Ticks")
        self.XMinorTicks_CB_StringVar = StringVar()
        self.XMinorTicks_CB.configure(variable=self.XMinorTicks_CB_StringVar, onvalue="yes", offvalue="no")
        self.XMinorTicks_CB_StringVar_traceName = self.XMinorTicks_CB_StringVar.trace_variable("w", self.XMinorTicks_CB_StringVar_Callback)
        self.XMinorTicks_CB_StringVar.set('yes')
        self.XMinorTicks_CB.pack(anchor=NW, side=TOP)

        # Y Axis linear/log choice
        self.YAxis_Labelframe = LabelFrame(self.a_frame,text="Y Axis:")

        self.YAxis_Linear_Radiobutton = Radiobutton(self.YAxis_Labelframe,text="Linear", 
            value="Linear", width="15", anchor=W)
        self.YAxis_Linear_Radiobutton.pack(anchor=NW, side=TOP)
        self.RadioGroup2_StringVar = StringVar()
        self.RadioGroup2_StringVar.set("Linear")
        self.RadioGroup2_StringVar_traceName = self.RadioGroup2_StringVar.trace_variable("w", self.RadioGroup2_StringVar_Callback)
        self.YAxis_Linear_Radiobutton.configure(variable=self.RadioGroup2_StringVar )

        self.YAxis_Log_Radiobutton = Radiobutton(self.YAxis_Labelframe,text="Log", 
            value="Log", width="15", anchor=W)
        self.YAxis_Log_Radiobutton.pack(anchor=NW, side=TOP)
        self.YAxis_Log_Radiobutton.configure(variable=self.RadioGroup2_StringVar )

        # Show Y Minor Log Ticks
        self.YMinorTicks_CB = Checkbutton(self.YAxis_Labelframe,text="Show logY Minor Ticks")
        self.YMinorTicks_CB_StringVar = StringVar()
        self.YMinorTicks_CB.configure(variable=self.YMinorTicks_CB_StringVar, onvalue="yes", offvalue="no")
        self.YMinorTicks_CB_StringVar_traceName = self.YMinorTicks_CB_StringVar.trace_variable("w", self.YMinorTicks_CB_StringVar_Callback)
        self.YMinorTicks_CB_StringVar.set('yes')
        self.YMinorTicks_CB.pack(anchor=NW, side=TOP)


        # Show title
        self.Title_Checkbutton = Checkbutton(self.a_frame,text="Show Plot Title")
        self.Title_Checkbutton_StringVar = StringVar()
        self.Title_Checkbutton.configure(variable=self.Title_Checkbutton_StringVar, onvalue="yes", offvalue="no")
        self.Title_Checkbutton_StringVar_traceName = self.Title_Checkbutton_StringVar.trace_variable("w", self.Title_Checkbutton_StringVar_Callback)
        self.Title_Checkbutton_StringVar.set('yes')
        
        # Show Grid
        self.Grid_Checkbutton = Checkbutton(self.a_frame,text="Show Plot Grid")
        self.Grid_Checkbutton_StringVar = StringVar()
        self.Grid_Checkbutton.configure(variable=self.Grid_Checkbutton_StringVar, onvalue="yes", offvalue="no")
        self.Grid_Checkbutton_StringVar_traceName = self.Grid_Checkbutton_StringVar.trace_variable("w", self.Grid_Checkbutton_StringVar_Callback)
        self.Grid_Checkbutton_StringVar.set('yes')
        
        # Show Legend
        self.Legend_Checkbutton = Checkbutton(self.a_frame,text="Show Legend")
        self.Legend_Checkbutton_StringVar = StringVar()
        self.Legend_Checkbutton.configure(variable=self.Legend_Checkbutton_StringVar, onvalue="yes", offvalue="no")
        self.Legend_Checkbutton_StringVar_traceName = self.Legend_Checkbutton_StringVar.trace_variable("w", self.Legend_Checkbutton_StringVar_Callback)
        self.Legend_Checkbutton_StringVar.set('yes')
        
        # Legend Location
        legLocL = ['best', 'upper right', 'upper left', 'lower left', 
            'lower right', 'right', 'center left', 
            'center right', 'lower center', 'upper center', 'center']
        self.Legend_Location_DD = Dropdown(self.a_frame,'Legend Location', legLocL,
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.Legend_Location_DD )

        # Legend Font
        self.Legend_Font_DD = Dropdown(self.a_frame,'Legend Font Size', 
            ['','8','9','10','11','12','13','14','16','18','20','22','24','36'],
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.Legend_Font_DD )

        # Legend Opacity
        self.Legend_Opacity_DD = Dropdown(self.a_frame,'Legend Opacity', 
            ['0.0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0'],default_val='0.5',
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.Legend_Opacity_DD )


        # B Frame =======================================================================
        # Show Points
        self.ShowPoints_Checkbutton = Checkbutton(self.b_frame,text="Show Points on Curves")
        self.ShowPoints_Checkbutton_StringVar = StringVar()
        self.ShowPoints_Checkbutton.configure(variable=self.ShowPoints_Checkbutton_StringVar, onvalue="yes", offvalue="no")
        self.ShowPoints_Checkbutton_StringVar_traceName = self.ShowPoints_Checkbutton_StringVar.trace_variable("w", self.ShowPoints_Checkbutton_StringVar_Callback)
        self.ShowPoints_Checkbutton_StringVar.set('yes')

        # Show Fat Lines
        self.Fatlines_Checkbutton = Checkbutton(self.b_frame,text="Fat Line on Extra Curves")
        self.Fatlines_Checkbutton_StringVar = StringVar()
        self.Fatlines_Checkbutton.configure(variable=self.Fatlines_Checkbutton_StringVar, onvalue="yes", offvalue="no")
        self.Fatlines_Checkbutton_StringVar_traceName = self.Fatlines_Checkbutton_StringVar.trace_variable("w", self.Fatlines_Checkbutton_StringVar_Callback)
        self.Fatlines_Checkbutton_StringVar.set('yes')

        # Number of Points on Curves
        self.NumPoints_DD = Dropdown(self.b_frame,'# Points in Curves', 
            ['100','200','300','400','500','600','700','800','900','1000','2000','3000','4000','5000','10000','20000','100000'],
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.NumPoints_DD )

        # Curve Point Size
        self.SizeCurvePoints_DD = Dropdown(self.b_frame,'Curve Point Size',  
            ['1','2','3','4','5','6','7','8','9','10'],default_val='2',
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.SizeCurvePoints_DD )

        # Curve Line Width
        self.WidthCurveLine_DD = Dropdown(self.b_frame,'Line Width',  
            ['1','2','3','4','5','6','7','8','9','10'],default_val='2',
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.WidthCurveLine_DD )
        

        # C Frame =======================================================================
        self.Weights_Checkbutton = Checkbutton(self.c_frame,text="Show Point Weights")
        self.Weights_Checkbutton_StringVar = StringVar()
        self.Weights_Checkbutton.configure(variable=self.Weights_Checkbutton_StringVar, onvalue="yes", offvalue="no")
        self.Weights_Checkbutton_StringVar_traceName = self.Weights_Checkbutton_StringVar.trace_variable("w", self.Weights_Checkbutton_StringVar_Callback)
        self.Weights_Checkbutton_StringVar.set('yes')


        # Data Point Size
        self.SizeDataPoints_DD = Dropdown(self.c_frame,'Data Point Size',
            ['6','7','8','9','10','11','12','13','14','16','18','20','22','24','36'], default_val='16',
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.SizeDataPoints_DD )

        # Data Point Type
        self.ColorDataPoint_DD = Dropdown(self.c_frame,'Data Point Color',
            ['red','blue','green','cyan','magenta','olive','darkorange','brown', 'darkviolet','gold','black'],
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.ColorDataPoint_DD )

        # Data Point Type
        self.pointStyleD = {'circle':'o','square':'s','star':'*','triangle':'^','diamond':'D','octagon':'8','pentagon':'p','hexagon':'H'}
            
        self.TypeDataPoints_DD = Dropdown(self.c_frame,'Data Point Type',
            ['circle','square','star','triangle','diamond','octagon','pentagon','hexagon'],
            callback=self.dd_callback, label_width='14')
        self.set_init_dropdown_value( self.TypeDataPoints_DD )

        #  Clipboard button
        self.customFont = tkinter.font.Font(family="Helvetica", size=14)        
        self.Clipboard_Button = Button(self.cc_frame,text="Put Plot on Clipboard")#,  font=self.customFont)
        self.Clipboard_Button.bind("<ButtonRelease-1>", self.Clipboard_Button_Click)
        
        # Save Plot to File Button
        self.PlotToFile_Button = Button(self.cc_frame,text="Save Plot to File")#,  font=self.customFont)
        self.PlotToFile_Button.bind("<ButtonRelease-1>", self.PlotToFile_Button_Click)

        # ======================== Start packing items =====================
        # Item packs in A Frame
        self.Title_Checkbutton.pack(anchor=NW, side=TOP)
        self.Grid_Checkbutton.pack(anchor=NW, side=TOP)
        self.Legend_Checkbutton.pack(anchor=NW, side=TOP)
        self.Legend_Location_DD.pack(anchor=NW, side=TOP)
        self.Legend_Font_DD.pack(anchor=NW, side=TOP)
        self.Legend_Opacity_DD.pack(anchor=NW, side=TOP)
        
        self.XAxis_Labelframe.pack(anchor=NW, side=TOP)
        self.YAxis_Labelframe.pack(anchor=NW, side=TOP)

        # Item packs in B Frame
        self.ShowPoints_Checkbutton.pack(anchor=NW, side=TOP)
        self.Fatlines_Checkbutton.pack(anchor=NW, side=TOP)
        self.NumPoints_DD.pack(anchor=NW, side=TOP)
        self.SizeCurvePoints_DD.pack(anchor=NW, side=TOP)
        self.WidthCurveLine_DD.pack(anchor=NW, side=TOP)

        # Item packs in C Frame
        self.Weights_Checkbutton.pack(anchor=NW, side=TOP)
        self.SizeDataPoints_DD.pack(anchor=NW, side=TOP)
        self.TypeDataPoints_DD.pack(anchor=NW, side=TOP)
        self.ColorDataPoint_DD.pack(anchor=NW, side=TOP)

        # frame packs
        self.a_frame.pack(anchor=NW, side=LEFT, padx=4, pady=4)
        self.b_frame.pack(anchor=NW, side=LEFT, padx=4, pady=4)
        self.c_frame.pack(anchor=NW, side=TOP, padx=4, pady=4)
        self.Clipboard_Button.pack(anchor=SE, side=BOTTOM, padx=4, pady=4)
        self.PlotToFile_Button.pack(anchor=SE, side=BOTTOM, padx=4, pady=4)
        self.cc_frame.pack(anchor=NW, side=LEFT, padx=4, pady=4, fill=Y, expand=1)
        
        # initialize attribute dictionary
        self.plotOptionD['XAxis'] = self.RadioGroup1_StringVar.get()
        self.plotOptionD['YAxis'] = self.RadioGroup2_StringVar.get()
        self.plotOptionD['ShowTitle'] = self.Title_Checkbutton_StringVar.get()
        self.plotOptionD['ShowGrid'] = self.Grid_Checkbutton_StringVar.get()
        self.plotOptionD['ShowLegend'] = self.Legend_Checkbutton_StringVar.get()
        self.plotOptionD['Weights'] = self.Weights_Checkbutton_StringVar.get()
                
        self.plotOptionD['ShowPoints'] = self.Fatlines_Checkbutton_StringVar.get()
        self.plotOptionD['FatLines'] = self.Fatlines_Checkbutton_StringVar.get()
        
        #print self.plotOptionD
    def PlotToFile_Button_Click(self, event):
        print('Save Plot to File')
        self.guiObj.PlotWin.toolbar.save_figure()


    def Clipboard_Button_Click(self, event):
        print('put plot on clipboard')
        self.guiObj.PlotWin.put_plot_on_clipboard()

    def refresh_last_plot(self):
        if hasattr(self.guiObj, 'PlotWin'):
            self.guiObj.PlotWin.refresh_last_plot()

    def set_init_dropdown_value(self, DD_obj):
        self.plotOptionD[DD_obj.label] = DD_obj.get_choice()

    def dd_callback(self, label, newvalue):
        print('From callback "%s"'%label,'=',newvalue)
        self.plotOptionD[label] = newvalue
        self.refresh_last_plot()

    def RadioGroup1_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['XAxis'] = self.RadioGroup1_StringVar.get()
        self.refresh_last_plot()


    def RadioGroup2_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['YAxis'] = self.RadioGroup2_StringVar.get()
        self.refresh_last_plot()
    
    def XMinorTicks_CB_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['XMinorTicks'] = self.XMinorTicks_CB_StringVar.get()
        self.refresh_last_plot()
    
    def YMinorTicks_CB_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['YMinorTicks'] = self.YMinorTicks_CB_StringVar.get()
        self.refresh_last_plot()
    
    def Title_Checkbutton_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['ShowTitle'] = self.Title_Checkbutton_StringVar.get()
        self.refresh_last_plot()

    def Grid_Checkbutton_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['ShowGrid'] = self.Grid_Checkbutton_StringVar.get()
        self.refresh_last_plot()
        
    def Legend_Checkbutton_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['ShowLegend'] = self.Legend_Checkbutton_StringVar.get()
        self.refresh_last_plot()


    def ShowPoints_Checkbutton_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['ShowPoints'] = self.ShowPoints_Checkbutton_StringVar.get()
        self.refresh_last_plot()

    def Fatlines_Checkbutton_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['FatLines'] = self.Fatlines_Checkbutton_StringVar.get()
        self.refresh_last_plot()

    def Weights_Checkbutton_StringVar_Callback(self, varName, index, mode):
        self.plotOptionD['Weights'] = self.Weights_Checkbutton_StringVar.get()
        self.refresh_last_plot()
