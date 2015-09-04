from future import standard_library
standard_library.install_aliases()
from builtins import range

from tkinter import *

class TabFrames(Frame):
    
    def __call__(self, N): #return frame widget of screen number N
        return self.pageFramesL[N]

    def setSelectCallback(self, N, callback): #set selecting callback of screen number N
        self.selectCallbackL[N] = callback

    def setLeaveCallback(self, N, callback): #set leaving callback of screen number N
        self.leaveCallbackL[N] = callback

    def __init__(self, master, tabPixelWidthL=None, labelL=None, 
        height=250, width=400, tabHeight=24, offx=4, offy=4):
            
        Frame.__init__(self,master)
        
        self.master = master
        self.tabPixelWidthL = tabPixelWidthL
        self.Ntabs = len( labelL )
        self.labelL = labelL
        self.tabHeight = tabHeight
        self.height = height
        self.width = width
        self.activeTab = None
        #self.activeFrame = None
        
        self.buttonL = []
        self.buttonIndexD = {} # get integer index into buttonL from button widget
        self.pageFramesL = []
        self.selectCallbackL = [] # call when selecting page
        self.leaveCallbackL = [] # call when leaving page
        
        # frame that holds TabFrames
        self.h, self.w = height+2*offy+tabHeight, width+2*offx
        frame =  Frame(self, height=self.h, width=self.w)
        self.dhlf, self.dwlf = self.h-height, self.w-width
        lframe =  LabelFrame(frame,text="", height=height, relief="groove", width=width)
        self.frame = frame
        self.lframe = lframe
        
        self.xlf = offx
        self.ylf = tabHeight+offy-2
        lframe.place(x=self.xlf, y=self.ylf, width=width, height=height)
        lframe.configure( borderwidth=4 )
        
        # make label buttons
        xb = offx * 2
        for N in range( self.Ntabs ):
            try:
                pw = tabPixelWidthL[N]
            except:
                pw = 40
            b = Button( frame, width="12", text=labelL[N] )
            b.bind("<ButtonRelease-1>", self.tabClicked)
            self.buttonL.append( b )
            self.buttonIndexD[b] = N 
            
            b.place( x=xb, y=offy, width=pw, height=tabHeight )
            b.configure( relief=SUNKEN )
            b.configure( borderwidth=2 )
            #b.configure( background="#dddddd" )
            b.lower(belowThis=self.lframe)
            #b.pack()
            xb += pw - 2
            
        # make frames for each page
        for N in range( self.Ntabs ):
            f = Frame( lframe )
            self.pageFramesL.append( f )
            self.selectCallbackL.append( None ) # start out assuming no callback
            self.leaveCallbackL.append( None )
            if N==0:
                f.pack(side=TOP, anchor=W, expand=YES, fill=BOTH)
                #self.activeFrame = f
            
        #self.frame.place(x=4,y=4,height=height, width=width)
        self.frame.pack(side=TOP, anchor=W, expand=YES, fill=BOTH)
        self.selectTab( self.buttonL[0] )
        
        self.frame.bind("<Configure>", self.ReConfigure)

    def ReConfigure(self, event):
        
        x = int(self.frame.winfo_x())
        y = int(self.frame.winfo_y())
        w = int(self.frame.winfo_width())
        h = int(self.frame.winfo_height())

        #print '#  -----------------   w,h=',w,h
        #print '#     self.w, self.h =',self.w, self.h
        #print '# winfo_reqwidth()=',self.winfo_width()
        #print '# winfo_reqheight()=',self.winfo_height()
        #self.lframe.config(width=w-self.dwlf, height=h-self.dhlf)
        
        self.lframe.place_forget()
        self.lframe.place(x=self.xlf, y=self.ylf, width=w-self.dwlf, height=h-self.dhlf)
        
    def tabClicked(self, event):
        #print 'tab clicked',event.widget
        #print 'selected tab = ', self.activeTab
        self.selectTab( event.widget )
        
    def selectTab(self, tab):
        if self.activeTab:
            b =  self.activeTab
            b.configure( relief=SUNKEN )
            b.configure( borderwidth=2 )
            #b.configure( background="#dddddd" )
            b.lower(belowThis=self.lframe)
            
            Nleave = self.buttonIndexD[self.activeTab]
            leaveCallback = self.leaveCallbackL[Nleave]
        else:
            leaveCallback = None
            
            
        #if self.activeFrame:
        #    self.activeFrame.forget()
        for fr in self.pageFramesL:
            fr.forget()
            
        self.activeTab = tab
        tab.configure( relief=RAISED )
        tab.configure( borderwidth=4 )
        #tab.configure( background="#ffffff" )
        tab.lift()
        
        N = self.buttonIndexD[tab]
        fr = self.pageFramesL[N]
        
        if leaveCallback:
            leaveCallback()
        
        callback = self.selectCallbackL[N]
        if callback:
            callback()
        
        fr.pack(fill=BOTH, expand=1)
        
        
        


if __name__ == '__main__':
    root = Tk()
    root.title('TabFrames Test')
    
    mainFrame = Frame(root, width=600, height=300)
    LF = LabelFrame(mainFrame,text="Frame to hold TabFrames")

    tf = TabFrames(LF, tabPixelWidthL=[90,120,60], labelL=['1234567890','xyzabcd','tab3'],
        width=600, height=200)
    
    page0 = tf(0)
    b = Button(page0, text='screen 0' )
    b.place( x=30, y=20 )
    b = Button(page0, text='screen 0B' )
    b.place( x=30, y=80 )
    
    page1 = tf(1)
    b = Button(page1, text='screen 1' )
    b.place( x=80, y=20 )
    b = Button(page1, text='screen 1B' )
    b.place( x=80, y=80 )
    
    page2 = tf(2)
    b = Button(page2, text='screen 2' )
    b.place( x=130, y=20 )
    b = Button(page2, text='screen 2B' )
    b.place( x=130, y=80 )
    
    #tf.place( 30, 30)
    tf.pack(anchor=NW, fill=BOTH, side=TOP, expand=True)
    #LF.place( x=20, y=20)
    LF.pack(anchor=NW, fill=BOTH, side=TOP, expand=True)
    mainFrame.pack(anchor=NW, fill=BOTH, side=TOP, expand=True)
    
    root.mainloop()
