from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range

from tkinter import *
import time
from xymath.gui.WtEntry_Dialog import _Wtentry

class WeightButton(Button):

    def __init__(self, master, i, wt_value=1.0, **kw):
        Button.__init__(*(self, master), **kw)
        
        self.set_float_val( wt_value )
        self.__i = i
    
    def get_wt_val(self):
        return self.__wt_value
    
    def set_float_val(self, fval):
        try:
            newval = float(fval)
        except:
            newval = 1.0
        self.__wt_value = newval
        
        #if abs(newval)-1.0 < 0.0001:
        #    self.configure(text='x %g'%newval)
        #else:
        self.configure(text='%g'%newval)
        
        if self.__wt_value < 0.9999:
            self.configure(bg="#7777ff")
        elif self.__wt_value > 1.0001:
            self.configure(bg="#ff7777")
        else:
            self.configure(bg="#cccccc")
            

class FloatEntry(Entry):
    # base class for validating entry widgets

    def __init__(self, master, i, j, grid_callback, value="", bg='', **kw):
        Entry.__init__(*(self, master), **kw)
        
        if bg:
            self.configure(bg=bg)
        self.__mybg = self.cget('bg')
        
        self.__i = i
        self.__j = j
        self.__grid_callback = grid_callback
            
        self.__strvar = StringVar()
        self.__strvar.trace("w", self.__callback)
        self.config(textvariable=self.__strvar)
        self.set_float_val( value )
        #self.__float_val = self.validate() # can be float or None
        #self.__strvar.set(value)
    
    def reset_bg(self):
        self.configure(bg=self.__mybg)
    
    def get_float_val(self):
        return self.__float_val
        
    def is_float(self):
        #print 'type(self.__float_val)',type(self.__float_val)
        return type(self.__float_val) is float
        
    def set_float_val(self, fval):
        if type(fval) is float:
            self.__strvar.set(fval)
        elif fval is None:
            self.__strvar.set('')
        else:
            #print '...converting "%s" to string'%fval
            self.__strvar.set( str(fval).strip() )
            

    def __callback(self, *dummy):
        self.__float_val = self.validate() # can be float or None
        if (self.__float_val is None) and self.__strvar.get():
            self.configure(bg="#ff7777") # show red if float is bad.
        else:
            self.configure(bg=self.__mybg)
            
        self.__grid_callback(self.__i, self.__j)
        #print '__strvar.get()="%s",__float_val="%s"'%(self.__strvar.get(), self.__float_val),type(self.__float_val)

    def validate(self):
        self.__strvar.set( self.__strvar.get().strip() )
        try:
            v = float(self.__strvar.get())
            return v
        except:
            return None

class EntryGrid(Frame):
    
    def grid_callback(self, i, j):
        '''Call here from Entry widget if its StringVar changes.'''
        
        if self.mode_init:
            return # if initializing, ignore StringVar changes
        
        #print '___in grid_callback i=%s, j=%s'%(i, j)
        self.page_callback(i,j)
    
    def is_a_good_row(self, i):
        if i>=self.Nrows:
            return False
        #print 'is_float()',self.entryL[i][0].is_float(), 'is_float()',self.entryL[i][1].is_float()
        return self.entryL[i][0].is_float() and self.entryL[i][1].is_float()
    
    def add_a_row(self):

        i = self.Nrows
        self.Nrows += 1
        self.entryL.append([])


        for j in range( self.Ncols ):
            if i%2==0:
                e = FloatEntry( self.entry_frame,i, j, self.grid_callback, width=10, bg=self.oddBG )
            else:
                e = FloatEntry( self.entry_frame,i, j, self.grid_callback, width=10 )
                
            self.entryL[i].append( e )
            
            if self.font:
                e.configure(font=self.font)
            if self.charWidthL:
                e.configure( width=self.charWidthL[j] )
            e.grid(row=i, column=j, sticky=W+E+N+S)
            
            #e.insert(0, 'R%i, C%i'%(i,j))
            #print 'R%i, C%i'%(i,j),'e.winfo_reqwidth()=',e.winfo_reqwidth()
            
            # set handler for each Entry widget
            def handler(event, self=self,   i=i, j=j):
                return self.ReturnKeyHandler( event,   i, j )
                
            self.entryL[i][j].bind("<Return>", handler)

            
            # set handler for each Entry widget
            def handler(event, self=self,   i=i, j=j):
                return self.ArrowKeyHandler( event,   i, j )
                
            self.entryL[i][j].bind("<Key>", handler)


        
        # set handler for each Weight Button
        def wtBtnHandler(event, self=self,   i=i):
            return self.WeightButtonHandler( event,  i)
        
        wb = WeightButton(self.entry_frame, i, width='8')#,text="x 1")
        wb.bind("<ButtonRelease-1>", wtBtnHandler)
        wb.grid(row=i, column=self.Ncols, sticky=W+E+N+S)
        self.entryL[i].append( wb )

        self.tot_entry_height += e.winfo_reqheight()
            
        self.entryL[i][0].focus_force()
        self.canv.config(scrollregion=(0,0,self.tot_entry_width, self.tot_entry_height+30))
        

    def __init__(self, master, page_callback, 
        Nrows=4, Ncols=3, charWidthL=None, labelL=None, 
        oddBG='#eeeeff', font='Courier 10 bold', horiz_scroll=0):
            
        self.mode_init = 1
        
        self.num_active_wtfactors = 0 # keep track of the number of weighting factors != 1
            
        Frame.__init__(self,master)
        
        self.page_callback = page_callback
        self.timeStamp = time.time() # can be used to track most recent entry
        
        self.master = master
        self.charWidthL = charWidthL
        
        self.Ncols = Ncols
        self.labelL = labelL
        self.font = font
        self.oddBG = oddBG
        
        # make canvases and frames
        self.canv_lab = canv_lab = Canvas(self, relief=SUNKEN)
        self.canv = canv = Canvas(self, relief=SUNKEN)
        
        # frame that holds EntryGrid
        self.entry_frame = ef = Frame(canv, relief=SUNKEN)
        self.labelFrame= lf = Frame(canv_lab, relief=SUNKEN)
        
        # make scroll bar objects
        vbar=Scrollbar(self,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=canv.yview)
        if horiz_scroll:
            hbar=Scrollbar(self,orient=HORIZONTAL, command=self.OnHorizScroll)
            hbar.pack(side=BOTTOM,fill=X)
            #hbar.config(command=canv.xview)
        
        
        # if labels are input, place them
        labelL.append('weight')
        charWidthL.append( 8 )
        wlab = 10 * Ncols
        hlab = 10
        if labelL:
            wlab = 0
            for j in range( Ncols+1 ):
                l = Entry( lf, width=10, justify=CENTER )
                l.insert(0, labelL[j])
                if charWidthL:
                    l.configure( width=charWidthL[j] )
                if font:
                    l.configure(font=font)
                    
                l.grid(row=0, column=j, sticky=W)
                
                self.normalbg = l.cget('bg')
                self.normalfg = l.cget('fg')
                
                l.configure(state=DISABLED, 
                    disabledbackground='#eeeeff', disabledforeground='#000000')
                wlab += l.winfo_reqwidth()
            hlab = l.winfo_reqheight() 
            
        lf.pack( side=LEFT, anchor=W )
        canv_lab.create_window(0,0,anchor=N+W,window=lf)
        
        # place Entry widgets into Grid
        self.tot_entry_height = 0
        self.tot_entry_width = wlab
        self.Nrows = 0
        
        # make 2D array to save entry widgets
        self.entryL = []
        for i in range( Nrows ):
            self.add_a_row()
        
        # tweek tot_entry_width for buttons
        #self.wt_button_width = self.entryL[1][-1].winfo_reqheight() 
        #self.tot_entry_width += self.wt_button_width * 2
            
        ef.pack( side=TOP, anchor=W, expand=True,fill=Y )
        canv.create_window(0,0,anchor=N+W,window=ef)
        
        #print 'tot ht=',self.tot_entry_height,'  tot w=',self.tot_entry_width
        
        if horiz_scroll:
            self.canv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            self.canv_lab.config(xscrollcommand=hbar.set)
        else:
            self.canv.config(yscrollcommand=vbar.set)
            
        canv_lab.pack(side=TOP, anchor=W)#,expand=True,fill=Y)
        canv.pack(side=TOP, anchor=W, expand=True,fill=Y)

        #self.pack(expand=True,fill=BOTH)
        
        canv_lab.config(width=wlab, height=hlab, scrollregion=(0,0,wlab, hlab))
        self.canv.config(scrollregion=(0,0,self.tot_entry_width, self.tot_entry_height+30))
        
        for obj in [self, canv, canv_lab, ef, lf]:
            obj.configure(width = self.tot_entry_width)
        
        #print 'self.normalbg =', self.normalbg 
        #print 'self.normalfg =',self.normalfg
        
        self.mode_init = 0


    def OnHorizScroll(self, *args):
        self.canv.xview(*args)
        self.canv_lab.xview(*args)

    def update_num_active_wtfactors(self, i, newval):
        wb = self.entryL[i][2]
        old_1 = abs(wb.get_wt_val() - 1.0) < 0.001
        new_1 = abs(newval - 1.0) < 0.001
        
        if new_1:
            if not old_1:
                self.num_active_wtfactors -= 1
        else:
            if old_1:
                self.num_active_wtfactors += 1

        self.entryL[i][2].set_float_val( newval )
        #print 'Number of Weighted Points =',self.num_active_wtfactors

    def WeightButtonHandler(self, event,   i):
        print('Clicked WeightButtonHandler for row',i)
        if self.is_a_good_row( i ):
            x,y = self.getValue(i,0), self.getValue(i,1)
            w = self.entryL[i][2].get_wt_val()
            
            dialog = _Wtentry(self.master, title="Point #%i Weighting Factor"%(i+1,), dialogOptions={'x':x, 'y':y,'w':w})
            print('===============Result from Dialog====================')
            print(dialog.result)
            print('=====================================================')
            if 'Weight' in dialog.result:
                try:
                    newval = float( dialog.result['Weight'] )
                    self.update_num_active_wtfactors(i, newval)
                except:
                    print('Return Value Error')
            
        else:
            print('No weighting of empty rows or rows with errors')



    def ArrowKeyHandler(self, event,   i, j ):
        
        print(event.keysym,'at i,j=',i,j)
        
        if event.keysym not in ['Up','Down','Left','Right']:
            return
            
        if event.keysym == 'Up':
            deli=-1
            delj=0
        elif event.keysym == 'Down':
            deli=1
            delj=0
        elif event.keysym == 'Right':
            deli=0
            delj=1
            if self.entryL[i][j].index(INSERT) < self.entryL[i][j].index(END):
                return
        else: # assume Left
            deli=0
            delj=-1
            if self.entryL[i][j].index(INSERT) > self.entryL[i][j].index(0):
                return
        
        jnext = j+delj
        inext = i+deli
        if jnext >= self.Ncols:
            jnext = 0
        if jnext<0:
            jnext = self.Ncols - 1
        if inext >= self.Nrows:
            inext = 0
        if inext<0:
            inext = self.Nrows - 1
                
        while self.entryL[inext][jnext].cget('state') == DISABLED:
            jnext += delj
            inext += deli
            if jnext >= self.Ncols or jnext<0:
                return
            if inext >= self.Nrows or inext<0:
                return
            
        self.entryL[inext][jnext].focus_force()
        
    def ReturnKeyHandler(self, event,   i, j ):
        jnext = j+1
        inext = i
        if jnext >= self.Ncols:
            jnext = 0
            inext = i+1
            if inext>=self.Nrows:
                self.add_a_row()
                
        while self.entryL[inext][jnext].cget('state') == DISABLED:
            jnext += 1
            if jnext >= self.Ncols:
                jnext = 0
                inext = i+1
                if inext>=self.Nrows:
                    inext = 0
            
        self.entryL[inext][jnext].focus_force()

    #def _grid(self, **kw):
    #    self.entry_frame.grid(kw)
    #    self.grid(kw)

    #def pack(self, **kw):
    #    self.entry_frame.pack(kw)
        
    #def place(self, x, y):
    #    self.entry_frame.place( x=x, y=y )
        
    def focus_on(self, i,j):
        return self.entryL[i][j].focus_force()
        
    def getValue(self, i,j):
        return self.entryL[i][j].get()
        
    def setValue(self, i,j, val, bg=None):
        self.entryL[i][j].delete(0, END)
        self.entryL[i][j].insert(END, val )
        if bg:
            self.entryL[i][j].configure(bg=bg)
        
    def makeReadOnly(self, i,j):
        if i%2==1:
            return self.entryL[i][j].configure(state=DISABLED, 
                disabledbackground=self.oddbg, disabledforeground='#000099')
        else:
            return self.entryL[i][j].configure(state=DISABLED, 
                disabledbackground=self.normalbg, disabledforeground='#000099')

    def bindKeyEntry(self, i, j, handler):
        #self.entryL[i][j].bind("<FocusOut>", handler)
        self.entryL[i][j].bind("<Key>", handler)

    def bindEventEntry(self, i, j, handler, eventName="<FocusIn>", newBG=None):
        self.entryL[i][j].bind(eventName, handler)
        
        if newBG:
            self.entryL[i][j].configure( bg=newBG )
    
    def setStringVar(self, i, j, svar):
        self.entryL[i][j].configure(textvariable=svar)
        
    def destroy(self):
        for i in range( self.Nrows ):
            for j in range( self.Ncols ):
                self.entryL[i][j].destroy()
                
        self.entryL = []
        self.Nrows = 0
        #self.entry_frame.destroy()
        

if __name__ == '__main__':
    root = Tk()
    root.title('EntryGrid Test')
    
    mainFrame = Frame(root, width=600, height=600, relief=SUNKEN)
    
    eg = EntryGrid(mainFrame, charWidthL=[10,15,10,6,12], labelL=['col1','col2','col3','xx','yy'], 
        Nrows=15, Ncols=5, horiz_scroll=1)
    eg.pack(expand=True,fill=BOTH)
    #eg.grid(row=0, column=0)
    mainFrame.pack( side=TOP, anchor=W, expand=True,fill=Y )
    
    root.mainloop()
