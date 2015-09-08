from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
import time
from tkinter import *
from xymath.gui.double_wt_entrygrid import EntryGrid
from numpy import array, double

def get_time_str( tstamp, label ):
    #return label + str( tstamp )
    return label + time.strftime(" TimeStamp: %m/%d/%Y %H:%M:%S", time.localtime(tstamp))

class PageData(object):
    
    def leavePageCallback(self):
        '''When leaving page, tidy up any XYjob issues.'''
        #print 'Leaving PageData'
        self.put_entry_values_on_plot()
        #self.guiObj.see_me() # force focus back
        
    def selectPageCallback(self):
        '''When entering page, do a little setup'''
        #self.eg.focus_on(0,0)
        if not self.block_entry_update:
            self.place_xyjob_data()
    
    def page_callback(self, i, j):
        '''Call here from EntryGrid if there is a change to one of its 
           Entry widget's StringVar items.'''
        if self.mode_place_xyjob:
            return # ignore callbacks if in mode_place_xyjob
            
        #print '___in page_callback i=%s, j=%s'%(i, j)
        
        if hasattr(self,'eg'):
            self.show_editor_timestamp()
            #if self.eg.is_a_good_row( i ):
            #    self.UpdatePlotButton.configure(state=NORMAL)
            #    self.put_entry_values_on_plot()
                
                #self.guiObj.master.deiconify()
                #self.guiObj.master.lift()
                #self.guiObj.master.focus_set()
                #self.guiObj.master.grab_set()
                
                #self.guiObj.master.lift()
                #self.eg.focus_on(i,j)

        return
    
    def put_entry_values_on_plot(self):
        
        self.place_entries_into_dataset()
        XY = self.guiObj.XYjob
        
        self.guiObj.PlotWin.make_new_plot(dataset=XY.dataset, curveL=[], 
            title_str='Data')
        
    def show_data_timestamp(self):
        self.Data_TimeStamp_Label.configure(text=get_time_str( self.guiObj.XYjob.dataset.timeStamp,'  Data' ))
        
    def show_editor_timestamp(self):
        self.eg.timeStamp = time.time()
        self.Editor_TimeStamp_Label.configure(text=get_time_str( self.eg.timeStamp, 'Editor' ))

    def place_entries_into_dataset(self):
        '''Put entry data into XYjob dataset'''

        xL = []
        yL = []
        wL = []
        for i in range(self.eg.Nrows):
            if self.eg.is_a_good_row( i ):
                xL.append( self.eg.entryL[i][0].get_float_val() )
                yL.append( self.eg.entryL[i][1].get_float_val() )
                if self.eg.num_active_wtfactors:
                    wL.append( self.eg.entryL[i][2].get_wt_val() )
                    print('adding',xL[-1],yL[-1],wL[-1])
                #else:
                #    print 'adding',xL[-1],yL[-1]
        
        if len(xL)>0:
            XY = self.guiObj.XYjob
            
            if self.eg.num_active_wtfactors:
                wtArr = array(wL, dtype=double)
            else:
                wtArr = None
                print('place_entries_into_dataset with wtArr = None')
            
            XY.define_dataset( array(xL, dtype=double), array(yL, dtype=double), wtArr=wtArr, 
                xName=self.Xname_Entry_StringVar.get(), yName=self.Yname_Entry_StringVar.get(),
                xUnits=self.Xunits_Entry_StringVar.get(), yUnits=self.Yunits_Entry_StringVar.get(), 
                timeStamp=self.eg.timeStamp)
                
            XY.dataset.sort_by_x()

    def place_xyjob_data(self):
        '''Put data from XYjob into PageData'''
        
        XY = self.guiObj.XYjob
        if not XY.dataset:
            return
        
        self.mode_place_xyjob = 1
        self.eg.timeStamp = XY.dataset.timeStamp
        self.show_data_timestamp()
        
        self.Xname_Entry_StringVar.set(XY.dataset.xName)
        self.Xunits_Entry_StringVar.set(XY.dataset.xUnits)
        self.Yname_Entry_StringVar.set(XY.dataset.yName)
        self.Yunits_Entry_StringVar.set(XY.dataset.yUnits)
        
        # put data into entry grid
        self.eg.focus_on(0,0)
        N = int( XY.dataset.N )
        # Add enough rows to hold data, if required
        if self.eg.Nrows <= N:
            for i in range( self.eg.Nrows, N+2):
                self.eg.add_a_row()
        
        num_active_wtfactors = 0
        
        for i in range(self.eg.Nrows):
            # clear all the entry locations
            if i < N: # only inserts value into entry for existing values
                self.eg.entryL[i][0].set_float_val(XY.dataset.xArr[i])
                self.eg.entryL[i][1].set_float_val(XY.dataset.yArr[i])
                
                if XY.dataset.wtArr is None:
                    #self.eg.entryL[i][2].set_float_val( 1.0 )
                    self.eg.update_num_active_wtfactors(i, 1.0)
                else:
                    #self.eg.entryL[i][2].set_float_val( XY.dataset.wtArr[i] )
                    self.eg.update_num_active_wtfactors(i, XY.dataset.wtArr[i])
                    if abs(1.0 - XY.dataset.wtArr[i]) > 0.001:
                        num_active_wtfactors += 1
                
            else:
                self.eg.entryL[i][0].set_float_val('')
                self.eg.entryL[i][1].set_float_val('')
                self.eg.entryL[i][2].set_float_val( 1.0 ) # do not impact num_active_wtfactors

        self.eg.num_active_wtfactors = num_active_wtfactors

        # Now show data points in plot
        self.put_entry_values_on_plot()

        # diable plot button
        #self.UpdatePlotButton.configure(state=DISABLED)

        # change mode flag back to 0
        self.mode_place_xyjob = 0

    def clear_all_data(self):
        '''Clear All PageData'''
        
        self.mode_place_xyjob = 1
        self.eg.timeStamp = time.time()
        self.Data_TimeStamp_Label.configure(text='')
        self.Editor_TimeStamp_Label.configure(text='')
        
        
        self.Xname_Entry_StringVar.set('x')
        self.Xunits_Entry_StringVar.set('')
        self.Yname_Entry_StringVar.set('y')
        self.Yunits_Entry_StringVar.set('')
        
        # put data into entry grid
        self.eg.focus_on(0,0)
        
        self.eg.num_active_wtfactors = 0
        
        for i in range(self.eg.Nrows):
            # clear all the entry locations
            if 1: #i < N: # only inserts value into entry for existing values
                self.eg.entryL[i][0].set_float_val('')
                self.eg.entryL[i][1].set_float_val('')
                self.eg.entryL[i][2].set_float_val( 1.0 ) # do not impact num_active_wtfactors
        
        # change mode flag back to 0
        self.mode_place_xyjob = 0

    def __init__(self, guiObj, pageFrame):
        
        self.mode_place_xyjob = 0
        self.block_entry_update = 0
        
        self.guiObj = guiObj
        self.pageFrame = pageFrame
        
        self.eg = EntryGrid(pageFrame, self.page_callback, 
            charWidthL=[12,12], labelL=['x-data','y-data'], 
            Nrows=15, Ncols=2, horiz_scroll=0)
            
        self.eg.pack(anchor=NW, side=LEFT, expand=True,fill=BOTH)
        self.eg.timeStamp = time.time()
        
        self.iframe = Frame(pageFrame)
        xframe = LabelFrame(self.iframe, text="", relief="groove")
        yframe = LabelFrame(self.iframe, text="", relief="groove")

        self.Data_TimeStamp_Label = Label(self.iframe,text="")
        self.Editor_TimeStamp_Label = Label(self.iframe,text="")

        self.Xname_Entry = Entry(xframe,width="15")
        self.Xname_Entry.grid(row=1, column=1, sticky=W)
        self.Xname_Entry_StringVar = StringVar()
        self.Xname_Entry.configure(textvariable=self.Xname_Entry_StringVar)
        self.Xname_Entry_StringVar.set("x")
        self.Xname_Entry_StringVar_traceName = \
            self.Xname_Entry_StringVar.trace_variable("w", self.Xname_Entry_StringVar_Callback)

        self.Xunits_Entry = Entry(xframe,width="15")
        self.Xunits_Entry.grid(row=2, column=1, sticky=W)
        self.Xunits_Entry_StringVar = StringVar()
        self.Xunits_Entry.configure(textvariable=self.Xunits_Entry_StringVar)
        self.Xunits_Entry_StringVar.set("")
        self.Xunits_Entry_StringVar_traceName = \
            self.Xunits_Entry_StringVar.trace_variable("w", self.Xunits_Entry_StringVar_Callback)

        self.Xname_Label = Label(xframe,text="X Name")
        self.Xname_Label.grid(row=1, column=0, sticky=W)

        self.Xunits_Label = Label(xframe,text="X Units")
        self.Xunits_Label.grid(row=2, column=0, sticky=W)
        
        self.Yname_Entry = Entry(yframe,width="15")
        self.Yname_Entry.grid(row=1, column=1, sticky=W)
        self.Yname_Entry_StringVar = StringVar()
        self.Yname_Entry.configure(textvariable=self.Yname_Entry_StringVar)
        self.Yname_Entry_StringVar.set("y")
        self.Yname_Entry_StringVar_traceName = \
            self.Yname_Entry_StringVar.trace_variable("w", self.Yname_Entry_StringVar_Callback)

        self.Yunits_Entry = Entry(yframe,width="15")
        self.Yunits_Entry.grid(row=2, column=1, sticky=W)
        self.Yunits_Entry_StringVar = StringVar()
        self.Yunits_Entry.configure(textvariable=self.Yunits_Entry_StringVar)
        self.Yunits_Entry_StringVar.set("")
        self.Yunits_Entry_StringVar_traceName = \
            self.Yunits_Entry_StringVar.trace_variable("w", self.Yunits_Entry_StringVar_Callback)

        self.Yname_Label = Label(yframe,text="Y Name")
        self.Yname_Label.grid(row=1, column=0, sticky=W)

        self.Yunits_Label = Label(yframe,text="Y Units")
        self.Yunits_Label.grid(row=2, column=0, sticky=W)
        
        xframe.pack(anchor=NW, side=TOP)
        yframe.pack(anchor=NW, side=TOP)
        self.Data_TimeStamp_Label.pack(anchor=NW, side=TOP)
        self.Editor_TimeStamp_Label.pack(anchor=NW, side=TOP)
        
        self.btn_frame = Frame(self.iframe)
        
        self.UpdatePlotButton = Button(self.btn_frame,text="Update Plot", width="15")
        self.UpdatePlotButton.bind("<ButtonRelease-1>", self.UpdatePlotButton_Click)
        self.UpdatePlotButton.pack(anchor=NW, side=LEFT)
        
        self.SwapXYButton = Button(self.btn_frame,text="Swap X and Y", width="15")
        self.SwapXYButton.bind("<ButtonRelease-1>", self.SwapXYButton_Click)
        self.SwapXYButton.pack(anchor=NW, side=LEFT)
        
        self.Btn_Space = Label(self.btn_frame,text=" ")
        self.Btn_Space.pack(anchor=NW, side=LEFT, fill=X, expand=1)
        
        
        #self.ShowHelpButton = Button(self.btn_frame,text="Show Help", width="15")
        #self.ShowHelpButton.bind("<ButtonRelease-1>", self.ShowHelp_Button_Click()
        #self.ShowHelpButton.pack(anchor=NE, side=LEFT)
        
        self.btn_frame.pack(anchor=NW, side=TOP, fill=X, expand=1)

        self.Label_Space = Label(self.iframe,text=" ")
        self.Label_Space.pack(anchor=NW, side=TOP)
        
        # make text resulsts area
        lbframe = Frame( self.iframe )
        self.Messages_Text_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Messages_Text = Text(lbframe, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Messages_Text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Messages_Text.pack(side=LEFT, fill=BOTH, expand=1)
        self.Messages_Text_frame.pack(anchor=NW, side=TOP, fill=BOTH, expand=1)

        
        
        self.iframe.pack(anchor=NW, side=LEFT, expand=True,fill=BOTH)
        slab = Label(pageFrame,text="  "*200) # pin xframe and yframe to the left
        slab.pack(anchor=E, side=LEFT, expand=True,fill=BOTH)
        
        self.ShowHelp_Button_Click(None)
        
    def ShowHelp_Button_Click(self, event):
        #print 'Pressed ShowHelp Button'
        self.new_message('''Enter X,Y data pairs into entry boxes 
at left. The boxes can be navigated with
the mouse, the return key or arrow keys.

All of the curve fitting options will use
these data.

To make curves go nearer certain points,
click the "weight" button next to that
point's entry boxes and enter a weight
greater than 1.

If names and units are entered for X
and Y, they will appear on plots.

Any edits will appear on plots when 
the "Update Plot" button is pressed, or 
when another tabbed page is selected.
''')
        
    def UpdatePlotButton_Click(self, event):
        if hasattr(self,'eg'):
            self.block_entry_update = 1
            self.put_entry_values_on_plot()
            self.block_entry_update = 0
    
    def SwapXYButton_Click(self, event):
        if hasattr(self,'eg'):
            self.guiObj.XYjob.dataset.swap_x_and_y()
            self.place_xyjob_data()
            self.show_editor_timestamp()
            #self.block_entry_update = 1
            #self.put_entry_values_on_plot()
            #self.block_entry_update = 0
    
    def Xname_Entry_StringVar_Callback(self, varName, index, mode):
        pass
        #print "Xname_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        #print "    new StringVar value =",self.Xname_Entry_StringVar.get()

    def Xunits_Entry_StringVar_Callback(self, varName, index, mode):
        pass
        #print "Xunits_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        #print "    new StringVar value =",self.Xunits_Entry_StringVar.get()

    def Yname_Entry_StringVar_Callback(self, varName, index, mode):
        pass
        #print "Yname_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        #print "    new StringVar value =",self.Yname_Entry_StringVar.get()

    def Yunits_Entry_StringVar_Callback(self, varName, index, mode):
        pass
        #print "Yunits_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        #print "    new StringVar value =",self.Yunits_Entry_StringVar.get()

    
    def clear_messages(self):
        self.Messages_Text.delete(1.0, END)
        self.Messages_Text.update_idletasks()
        
    def add_to_messages(self, s):
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        
    def new_message(self, s):
        self.clear_messages()
        self.Messages_Text.insert(END, s)
        self.Messages_Text.update_idletasks()
        