#!/usr/bin/env python


from __future__ import print_function
from __future__ import absolute_import
import os
import sys
if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    import tkFileDialog
    import tkMessageBox
else:
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox
from builtins import str
from builtins import range
from builtins import object
import time
from numpy import array, double
from tkinter import *

from xymath.gui.tabframes import TabFrames
from xymath.gui.pagedata import PageData
from xymath.gui.page_simple_fit import SimplePage
from xymath.gui.page_spline import SplinePage
from xymath.gui.page_math import  MathPage
from xymath.gui.page_exhaust_fit import ExhaustPage
from xymath.gui.page_nonlin_fit import NonLinFitPage
from xymath.gui.page_plot import PagePlot # sets plot attributes
from xymath.gui.page_codegen import CodeGenPage

from xymath.gui.plot_window import PlotWindow
from xymath.gui.About_Dialog import _About
from xymath.gui.ImportXY_Dialog import _Importxy

from xymath.xy_job import XY_Job

LICENSE = '''
XYmath  Copyright (C) 2013  Charlie Taylor
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.'''

class _Xygui(object):
    
        
    def cleanupOnQuit(self):
        if (not self.has_some_data()) or \
            self.AskYesNo( title='Data Saved Before Quitting?', \
            message='Do you want to exit XYmath?\n(Hit "Yes" ONLY IF your data is saved.)'):
            
            print('Doing final cleanup before quitting')
            
            
            self.allow_subWindows_to_close = 1
            try:
                self.PlotWin.cleanupOnQuit()
            except:
                pass
                
            try:
                self.master.destroy()  # called in PlotWin
            except:
                pass
            sys.exit(1)
    
    #def see_me(self):
    #    '''Hoping to force focus back to main window.'''
    #    print 'Hope to see you back at main.'
    #    self.master.geometry( '%dx%d+%i+%i'%(self.master.winfo_width(),self.master.winfo_height(),
    #        self.master.winfo_x(),self.master.winfo_y()))
        
    def __init__(self, master, XYjob_inp=None):
        self.initComplete = 0
        #frame = Frame(master, width=753, height=536)
        #frame.pack()
        self.master = master
        self.allow_subWindows_to_close = 0
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        # bind master to <Configure> in order to handle any resizing, etc.
        # postpone self.master.bind("<Configure>", self.Master_Configure)
        self.master.bind('<Enter>', self.bindConfigure)
        

        self.master.title("XYmath")
        
        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.master, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)


        self.statusMessage.set("Welcome to XYmath")
        self.menuBar = Menu(master, relief = "raised", bd=2)

        top_File = Menu(self.menuBar, tearoff=0)

        top_File.add("command", label = "New", command = self.menu_File_New)
        top_File.add("command", label = "Open", command = self.menu_File_Open)
        top_File.add("command", label = "Import", command = self.menu_File_Import)
        top_File.add("command", label = "Save", command = self.menu_File_Save)
        top_File.add("command", label = "Exit", command = self.menu_Program_Exit)
        
        self.menuBar.add("cascade", label="File", menu=top_File)
        self.menuBar.add("command", label = "About", command = self.menu_About)



        self.tab_frames = TabFrames(self.master, height=460, width=650,
            tabPixelWidthL=[60,90,       60,      60,       110,           110,        60,    90], 
            labelL=['Data','Simple Fit','Spline','Math','Exhaustive Fit','Non-Linear Fit','Plot','Code Gen'])
        self.tab_frames.pack(anchor=NW, fill=BOTH, side=TOP, expand=True)
        
        # Main window is finished, start building tab_frames pages
        self.pageD = {} # dictionary of tab_frames pages
        
        def setup_page( npage, PageObj ):
            self.pageD[npage] = PageObj(self, self.tab_frames(npage))
            self.pageD[ str(self.tab_frames.labelL[npage]) ] = self.pageD[npage]
            self.tab_frames.setLeaveCallback(npage, self.pageD[npage].leavePageCallback)
            self.tab_frames.setSelectCallback(npage, self.pageD[npage].selectPageCallback)
        
        # setup pages
        setup_page(0, PageData)    # setup page 0, Data page
        setup_page(1, SimplePage)  # setup page 1, Simple Curve Fit
        setup_page(2, SplinePage)  # setup page 2, Spline Curve Fit
        setup_page(3, MathPage)    # setup page 3, Math Page
        setup_page(4, ExhaustPage) # setup page 4, Exhaustive Fit 
        setup_page(5, NonLinFitPage) # setup page 5, Non-Linear Fit 
        setup_page(6, PagePlot ) # setup page 6, PagePlot
        setup_page(7, CodeGenPage) # setup page 7, Code Generation Page

        master.config(menu=self.menuBar)
        
        if XYjob_inp is None:
            self.XYjob = XY_Job() # XYjob may hold nonlinear fit object
        else:
            self.XYjob = XYjob_inp
            
        self.linear_fitL = [] # list of candidate linear fits
        self.selected_spline_objL = [] # list of candidate spline fits
        
        if self.XYjob.nonlin_fit:
            self.pageD['Non-Linear Fit'].EqnStr_Text.delete(1.0, END)
            self.pageD['Non-Linear Fit'].EqnStr_Text.insert(END, self.XYjob.nonlin_fit.rhs_eqnStr)

        # check for input file on command line
        if (XYjob_inp is None) and (len( sys.argv ) == 2):
            fName = sys.argv[1]
            if not fName.endswith('.x_y'):
                fName += '.x_y'
            self.pathopen = os.path.abspath(fName)
            if os.path.isfile( self.pathopen ): # if file exists, read it as a definition file
                fInp = open( os.path.abspath(fName), 'rb' )
                self.read_xyjob_from_file(fInp)
            else:
                # For erroneous file names, change status bar
                self.statusMessage.set("file:%s NOT FOUND"%fName)

        # Enter Data page to begin with
        #self.tab_frames.selectTab( self.tab_frames.buttonL[0] )
        master.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)
        
        milliseconds=100
        self.master.after( milliseconds, self.littleInits )
        
        print(LICENSE)

    def littleInits(self):
        self.PlotWin = PlotWindow(self.master, self)
        
        self.tab_frames.selectTab( self.tab_frames.buttonL[0] )
        self.pageD[0].eg.focus_on(0,0)
        
        # If transient, will minimize with main window AND be drawn on top
        #self.PlotWin.transient(self.master) 
        
    def menu_Program_Exit(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Program_Exit"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Program_Exit")
        print("called menu_Program_Exit")
        
        self.cleanupOnQuit()

    def has_some_data(self):
        '''Return True if there is some data or curve fit being held in memory.'''
        print('Entering MathPage')
        XY = self.XYjob
        got_data = False
        
        if XY.nonlin_fit:
            print('Has a Non-Linear Fit')
            got_data = True
        
        for pagename in ['Simple Fit','Exhaustive Fit']:
            selected_linfitL = self.pageD[pagename].selected_linfitL
            for n,i in enumerate(selected_linfitL):
                print('Has a %s'%pagename)
                got_data = True
        
        for spline in self.selected_spline_objL:
            print('Has a Spline Fit')
            got_data = True
        
        DataPage = self.pageD['Data']
        if DataPage.Xname_Entry_StringVar.get() != 'x':
            print('Has x Name')
            got_data = True
        if DataPage.Xunits_Entry_StringVar.get() != '':
            print('Has x Units')
            got_data = True
        if DataPage.Yname_Entry_StringVar.get() != 'y':
            print('Has y Name')
            got_data = True
        if DataPage.Yunits_Entry_StringVar.get() != '':
            print('Has Y Units')
            got_data = True
            
        if DataPage.eg.num_active_wtfactors:
            print('Has Weight Factors')
            got_data = True
        
        for i in range(DataPage.eg.Nrows):
            if DataPage.eg.entryL[i][0].is_float() or DataPage.eg.entryL[i][1].is_float():
                print('Has Data in Entry Box')
                got_data = True
        
        if (not self.XYjob.dataset is None) or (not self.XYjob.linfit is None) or (not self.XYjob.nonlin_fit is None):
            print('Has Initialized XYjob')
            got_data = True
            
        
        return got_data

    def clear_all_data(self):

        self.XYjob = XY_Job() # XYjob may hold nonlinear fit object
        self.linear_fitL = [] # list of candidate linear fits
        self.selected_spline_objL = [] # list of candidate spline fits

        for pagename in ['Simple Fit','Exhaustive Fit']:
            self.pageD[pagename].selected_linfitL = []
            self.pageD[pagename].Equations_Listbox.delete(0, END)
            self.pageD[pagename].Pcentstddev_Listbox.delete(0, END)
            self.pageD[pagename].Stddev_Listbox.delete(0, END)


        self.pageD['Data'].clear_all_data()
            
        self.pageD['Code Gen'].Listbox_1.delete(0, END)
        self.pageD['Math'].Listbox_1.delete(0, END)
        self.pageD['Spline'].Listbox_1.selection_clear(0, 5)
        
        
        # remove any constant entry widgets and pack_forget Improve Button
        self.pageD['Non-Linear Fit'].ImproveFit_Button.pack_forget()
        self.pageD['Non-Linear Fit'].SetConst_Button.pack_forget()
        
        for e in self.pageD['Non-Linear Fit'].constEntryWidgetL:
            e.pack_forget()
            del(e)
        
        for pagename in ['Data','Simple Fit','Spline','Math','Exhaustive Fit','Non-Linear Fit','Code Gen']:
            self.pageD[pagename].ShowHelp_Button_Click(None)
            self.pageD[pagename].pageFrame.update_idletasks()
        
        
        self.PlotWin.start_new_plot()
        #self.PlotWin.add_curve([1,2,3],[4,6,9], label='Sample Data', show_pts=1, show_line=1, 
        #    linewidth=2, markersize=20)
        #self.PlotWin.final_touches( title_str='Sample Plot', show_grid=True, show_legend=True)
        self.PlotWin.show_it()
        

    def menu_File_New(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_New"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_New")
        print("called menu_File_New")
        if self.has_some_data():
            print('Has Some Data to be Cleared')
            if self.AskYesNo( title='Clear All Data', message='Do you want to clear all data from memory?'):
                self.clear_all_data()

    def menu_File_Open(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_Open"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_Open")
        print("called menu_File_Open")
        
        fInp = self.AskOpenFile(title='Open XYmath File', mode='rb', initialdir='.')
        if fInp:
            self.clear_all_data()
            self.read_xyjob_from_file(fInp)
            
    def read_xyjob_from_file(self, fInp):
        print('Opened file', os.path.basename( fInp.name ))
        # fInp will be closed by read_job_from_file
        self.XYjob.read_job_from_file(fileObj=fInp)
        #self.pageD['Data'].place_xyjob_data()
        prefix = os.path.basename(self.XYjob.file_prefix)
        self.master.title("XYmath - %s"%prefix)
        name = os.path.basename(self.XYjob.file_name)
        self.statusMessage.set("Read file:%s"%name)
        
        if hasattr(self,'PlotWin'):
            self.pageD['Data'].place_xyjob_data()
            
    def menu_File_Save(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_Save"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_Save")
        print("called menu_File_Save")
        
        if self.XYjob.file_prefix:
            initialfile = self.XYjob.file_prefix + '.x_y'
        else:
            initialfile = '*.x_y'
        
        fsave = self.AskSaveasFilename(title='Save XYmath File', initialfile=initialfile)
        
        if fsave:
            if not fsave.lower().endswith('.x_y'):
                fsave += '.x_y'
            
            self.pageD['Data'].put_entry_values_on_plot()
            
            self.XYjob.write_job_to_file( fname=fsave )
            print('Saving XYmath to:',fsave)
            prefix = os.path.basename(self.XYjob.file_prefix)
            self.master.title("XYmath - %s"%prefix)
            name = os.path.basename(self.XYjob.file_name)
            self.statusMessage.set("Read file:%s"%name)

    def bindConfigure(self, event):
        if not self.initComplete:
            self.master.bind("<Configure>", self.Master_Configure)
            self.initComplete = 1


    def Master_Configure(self, event):
        if event.widget != self.master:
            if self.w != -1:
                return
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        w = int(self.master.winfo_width())
        h = int(self.master.winfo_height())
        if (self.x, self.y, self.w, self.h) == (-1,-1,-1,-1):
            self.x, self.y, self.w, self.h = x,y,w,h


        if self.w!=w or self.h!=h:
            print("Master reconfigured... make resize adjustments")
            self.w=w
            self.h=h
            
        #print '  -----------------   w,h=',w,h
        #self.tab_frames.lframe.configure(width=w, height=h)
        #self.tab_frames.frame.configure(width=w, height=h)
        #print 'winfo_reqwidth()=',self.tab_frames.winfo_reqwidth()
        #print 'winfo_reqheight()=',self.tab_frames.winfo_reqheight()
        #self.master.update_idletasks()

    # standard message dialogs... showinfo, showwarning, showerror
    def ShowInfo(self, title='Title', message='your message here.'):
        tkMessageBox.showinfo( title, message )
        return
    def ShowWarning(self, title='Title', message='your message here.'):
        tkMessageBox.showwarning( title, message )
        return
    def ShowError(self, title='Title', message='your message here.'):
        tkMessageBox.showerror( title, message )
        return
        
    # standard question dialogs... askquestion, askokcancel, askyesno, or askretrycancel
    # return True for OK, Yes, Retry, False for Cancel or No
    def AskYesNo(self, title='Title', message='your question here.'):
        return tkMessageBox.askyesno( title, message )
    def AskOK_Cancel(self, title='Title', message='your question here.'):
        return tkMessageBox.askokcancel( title, message )
    def AskRetryCancel(self, title='Title', message='your question here.'):
        return tkMessageBox.askretrycancel( title, message )
        
    # return "yes" for Yes, "no" for No
    def AskQuestion(self, title='Title', message='your question here.'):
        return tkMessageBox.askquestion( title, message )
    # standard file dialogs... askdirectory, askopenfile, asksaveasfilename

    # return a string containing directory name
    def AskDirectory(self, title='Choose Directory', initialdir="."):
        dirname = tkFileDialog.askdirectory(parent=self.master,initialdir=initialdir,title=title)
        return dirname # <-- string
        
    # return an OPEN file type object OR None (opened using mode, 'r','rb','w','wb')
    # WARNING... opening file with mode 'w' or 'wb' will erase contents
    def AskOpenFile(self, title='Open XYmath File', mode='rb', initialdir='.', filetypes=None):
        if filetypes is None:
            filetypes = [
                ('XYmath File','*.x_y'),
                ('Any File','*.*')]
        fileobj = tkFileDialog.askopenfile(parent=self.master,mode=mode,title=title,
            initialdir=initialdir, filetypes=filetypes)
        
        # if opened, then fileobj.name contains the name string
        return fileobj # <-- an opened file, or the value None
        
    # return a string containing file name (the calling routine will need to open the file)
    def AskSaveasFilename(self, title='Save File', filetypes=None, initialfile=''):
        if filetypes is None:
            filetypes = [
                ('XYmath File','*.x_y'),
                ('Any File','*.*')]

        fileName = tkFileDialog.asksaveasfilename(parent=self.master,filetypes=filetypes, initialfile=initialfile ,title=title)
        return fileName # <-- string
        
    # alarm function is called after specified number of milliseconds
    def SetAlarm(self, milliseconds=1000):
        self.master.after( milliseconds, self.Alarm )
    def Alarm(self): 
        pass

        # >>>>>>insert any user code below this comment for section "standard_alarm"
        print("Alarm called")
        
    def menu_File_Import(self):
        dialog = _Importxy(self.master, "Import X,Y Data")
        if dialog.result:
            wtArr = None
            print('place_entries_into_dataset with wtArr = None')
            xL = dialog.result["xL"]
            yL = dialog.result["yL"]
            
            XY = self.XYjob
            XY.define_dataset( array(xL, dtype=double), array(yL, dtype=double), wtArr=wtArr, 
                xName=dialog.result["xName"], yName=dialog.result["yName"],
                xUnits='', yUnits='', 
                timeStamp=time.time())
                
            XY.dataset.sort_by_x()
            
            self.pageD['Data'].place_xyjob_data()

    def menu_About(self):
        dialog = _About(self.master, "About XYmath")
            

def main(XYjob_inp=None):
    root = Tk()
    app = _Xygui(root, XYjob_inp=XYjob_inp)
    root.mainloop()

if __name__ == '__main__':
    main()
