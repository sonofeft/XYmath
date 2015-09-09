#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import next
from builtins import zip
from builtins import object
from past.utils import old_div
from tkinter import *
import time

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from pylab import *

from PIL import Image
import io
try:
    import win32clipboard
except:
    print('WARNING... win32clipboard did NOT import properly.')

#colorL = ['red','green','blue','cyan','magenta','olive','brown','coral','gold']

colorL = ['r','g','b','m','c','olive','darkorange','brown',
    'darkviolet','black','gold']

def nextColor(): # color iterator for plots
    i = 0
    while i<len(colorL):
        yield colorL[i]
        i += 1
        
    r,g,b = 0.5,0.,0.
    f = 1.
    while 1:
        yield r,g,b
        yield b,r,g
        yield g,b,r
        if g>0.0:
            b = f
        g = f
        f = old_div(f,2.)


class BoxMessage(object):
    def __init__(self, xpt, ypt, message):
        self.xpt = xpt
        self.ypt = ypt
        self.message = message
        
    def place_it(self, ax):
        ax.text(self.xpt, self.ypt, self.message, 
            bbox={'facecolor':'#ccccff', 'alpha':0.5, 'pad':10})
        
        

class Annotation(BoxMessage):
    def __init__(self, xpt, ypt, message, xmess=None, ymess=None):
        BoxMessage.__init__(self, xpt, ypt, message)
        self.xmess= xmess
        self.ymess= ymess
        self.bbox_args = dict(boxstyle="round", fc="0.8", alpha=0.5)
        self.arrow_args = dict(arrowstyle="->")
        
    def place_it(self, ax, dx=None, dy=None):
        
        if (self.xmess is None) and (not dx is None):
            self.xmess = self.xpt + dx
            self.ymess = self.ypt + dy
        
        # if there are not message coords, just use a box
        if self.xmess is None:
            ax.text(self.xpt, self.ypt, self.message, va='center', ha='center',
                bbox={'facecolor':'#ccccff', 'alpha':0.5, 'pad':10})
        else:
            if self.xmess < self.xpt:
                haStr = 'left'
            else:
                haStr = 'right'
            if self.ymess < self.ypt:
                vaStr = 'bottom'
            else:
                vaStr = 'top'
            
            print('(self.xpt, self.ypt)=',(self.xpt, self.ypt))
            print('(self.xmess, self.ymess)=',(self.xmess, self.ymess))
            
            ax.annotate(self.message, 
                xy=(self.xpt, self.ypt),  #xycoords=ax.transData,
                xytext=(self.xmess, self.ymess), 
                horizontalalignment=haStr, verticalalignment=vaStr,
                #bbox=self.bbox_args,
                arrowprops=self.arrow_args )
        

class PlotWindow( Toplevel ):
    
    def add_annotation(self):
        
        bbox_args = dict(boxstyle="round", fc="0.8", alpha=0.5)
        arrow_args = dict(arrowstyle="->")

        self.ax.annotate('xy=(2.8, 3.5)\nxycoords=ax1.transData',
            xy=(2.8, 3.5),  xycoords=self.ax.transData,
            xytext=(3.5, 3.5), 
            ha="left", va="bottom",
            bbox=bbox_args,
            arrowprops=arrow_args )
        
        self.ax.text(3, 8, 'boxed text in data coords', 
            bbox={'facecolor':'#ccccff', 'alpha':0.5, 'pad':10})
    
    def refresh_last_plot(self):
        '''Refresh last plot.  Usually for a plot attribute change.'''
        if self.last_dataset or self.last_curveL:
            self.make_new_plot(dataset=self.last_dataset, curveL=self.last_curveL, 
                title_str=self.last_title_str, 
                xaxis_str=self.last_xaxis_str, yaxis_str=self.last_yaxis_str, 
                annotationL=self.last_annotationL, integFill=self.last_integFill,
                specialPtL=self.last_specialPtL, textLabelCurveL=self.last_textLabelCurveL,
                force_linear_y=self.last_force_linear_y)
    
    def make_new_plot(self, dataset=None, curveL=None, title_str='', 
        xaxis_str='', yaxis_str='', annotationL=None, integFill=None,
        specialPtL=None, dataLabel='Data', textLabelCurveL=None, force_linear_y=False):
        '''Make a new plot.
        
           integFill is a pair of x,y arrays to plot with shaded area to y=0.0
           specialPtL is a list of tuples (xArr, yArr, marker, markersize, label)
           annotationL is a list of BoxMessage and Annotation objects to add.
           textLabelCurveL is a list of tuples (xArr, yArr, color, linewidth, linetype, label)
        '''
        
        #print 'self.state()=',self.state()
        if self.state()=='iconic':
            self.state(newstate='normal')
        
        # save inputs for refresh_last_plot command
        self.last_dataset = dataset
        self.last_curveL = curveL
        self.last_title_str = title_str
        self.last_xaxis_str = xaxis_str
        self.last_yaxis_str = yaxis_str
        self.last_annotationL = annotationL
        self.last_integFill = integFill
        self.last_specialPtL = specialPtL
        self.last_textLabelCurveL = textLabelCurveL
        self.last_force_linear_y = force_linear_y
        
        
        self.force_linear_y = force_linear_y
        
        # get plot attributes from PagePlot
        Npoints = int( self.plotOptionD['# Points in Curves'] )
        show_grid = self.plotOptionD['ShowGrid'] == 'yes'
        show_legend = self.plotOptionD['ShowLegend'] == 'yes'
        show_title = self.plotOptionD['ShowTitle'] == 'yes'
        
        self.logx = self.plotOptionD['XAxis'] == 'Log'
        self.logy = (self.plotOptionD['YAxis'] == 'Log') and (not force_linear_y)
        
        showWeights = self.plotOptionD['Weights'] == 'yes'
        markersize = int( self.plotOptionD['Data Point Size'] )
        marker = self.pointStyleD[ self.plotOptionD['Data Point Type'] ]
        
        curve_markersize = int( self.plotOptionD['Curve Point Size'] )
        curve_lw =  int( self.plotOptionD['Line Width'] )
        
        showCurvePoints = self.plotOptionD['ShowPoints'] == 'yes'
        fat_lines = self.plotOptionD['FatLines'] == 'yes'
        
        if not show_title:
            title_str = ''
        
        # if no dataset is included in input, use a fitted curves dataset
        if not dataset and curveL:
            dataset = curveL[0].dataset
        
        # start a new plot
        self.start_new_plot()
        
        # put dataset on plot
        if dataset and dataset.N > 1:
            xaxis_str = dataset.get_x_desc()
            yaxis_str = dataset.get_y_desc()        
            self.add_curve( dataset.xArr, dataset.yArr, label=dataLabel, show_pts=1,
                show_line=0, linewidth=2, markersize=markersize, 
                color=self.plotOptionD['Data Point Color'], marker=marker)
                
            if (not dataset.wtArr is None) and showWeights:
                xwL=[]
                ywL=[]
                wwL=[]
                xwloL=[]
                ywloL=[]
                wwloL=[]
                for i,w in enumerate( dataset.wtArr ):
                    if w > 1.0:
                        xwL.append( dataset.xArr[i] )
                        ywL.append( dataset.yArr[i] )
                        wwL.append( w )
                    elif w < 1.0:
                        xwloL.append( dataset.xArr[i] )
                        ywloL.append( dataset.yArr[i] )
                        wwloL.append( w )
                        
                if xwL:
                    print('Adding Weighted Points to Plot.')
                    self.add_curve( xwL, ywL, label='Weighted High', show_pts=1,
                        show_line=0, markersize=markersize+5, marker='s', marker_alpha=0.5)
                    for x,y,w in zip(xwL,ywL,wwL):
                        self.ax.text(x,y,'  x%g'%w, va='center', ha='left')
                        
                if xwloL:
                    print('Adding Weighted Points to Plot.')
                    self.add_curve( xwloL, ywloL, label='Weighted Low', show_pts=1,
                        show_line=0, markersize=markersize+5, marker='d', marker_alpha=0.5)
                    for x,y,w in zip(xwloL,ywloL,wwloL):
                        self.ax.text(x,y,'  x%g'%w, va='center', ha='left')
                    
                    
        if xaxis_str=='':
            xaxis_str = 'X'
        if yaxis_str=='':
            yaxis_str = 'Y'
        
        # put curves on plot
        if curveL:
            for i,c in enumerate(curveL):
                xPlotArr, yPlotArr = c.get_xy_plot_arrays( Npoints=Npoints, logScale=self.logx)
                
                if fat_lines:
                    lw = curve_lw + int(old_div((len(curveL) - i),2))
                else:
                    lw = curve_lw
                    
                self.add_curve( xPlotArr, yPlotArr, label=c.name, 
                    show_pts=showCurvePoints, show_line=1, linewidth=lw, markersize=curve_markersize, integFill=integFill)
        
        # add any specialPtL items to plot
        if specialPtL:
            for xArr, yArr, marker, markersize, label in specialPtL:
                self.add_curve( xArr, yArr, label=label, show_pts=1, 
                    show_line=0, linewidth=2, markersize=markersize, marker=marker)
                
        if textLabelCurveL:
            for xArr, yArr, color, linewidth, linetype, label in textLabelCurveL:
                self.add_curve( xArr, yArr, label=label, show_pts=0, linetype=linetype,
                    show_line=1, linewidth=linewidth, color=color)
        
        
        self.final_touches( title_str=title_str, show_grid=show_grid, 
            show_legend=show_legend, xaxis_str=xaxis_str, yaxis_str=yaxis_str)
        
        if annotationL:
            for a in annotationL:
                if isinstance(a, Annotation):
                    if a.xpt>self.xmid:
                        dx = -self.dx * 5
                    else:
                        dx = self.dx * 5
                    if a.ypt>self.ymid:
                        dy = -self.dy * 5
                    else:
                        dy = self.dy * 5
                    a.place_it(self.ax, dx=dx, dy=dy)
                else:
                    a.place_it(self.ax)
        
        self.show_it()
        
        
    def cleanupOnQuit(self):
        if 0:# self.guiWin.allow_subWindows_to_close:
            # eliminate hanging when closing window
            try:
                self.master.destroy()
            except:
                pass
            sys.exit(1)
        
        self.wm_state('iconic')
    
    def __init__(self, master, guiWin):
        
        Toplevel.__init__(self, master)#, bg='#90EE90')#'lightgreen': '#90EE90',
        self.title('Plot Window')
        
        x = master.winfo_x()  + master.winfo_width() + 20
        #if x<10: x=10
        y = master.winfo_y() 
        #if y<370: y=370
        # position over to the upper right 
        self.geometry( '%dx%d+%i+%i'%(600,600,x,y))
        
        self.plotOptionD = guiWin.pageD['Plot'].plotOptionD
        self.pointStyleD = guiWin.pageD['Plot'].pointStyleD
        
        self.force_linear_y = False
        
        self.guiWin = guiWin
        self.master = master

        self.frame4 = Frame(self)
        self.frame4.pack(side=BOTTOM, anchor=W)#, fill=X, expand=1)
        self.frame3 = Frame(self)
        self.frame3.pack(side=TOP, fill=BOTH, expand=1)
        
        self.last_dataset = None
        self.last_curveL = None
        
        self.start_new_plot()
        self.add_curve([1,2,3],[4,6,9], label='Sample Data', show_pts=1, show_line=1, 
            linewidth=2, markersize=20)
        self.final_touches( title_str='Sample Plot', show_grid=True, show_legend=True)
        self.show_it()

        # only main window can close this window
        self.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)
        
    def start_new_plot(self):
        '''Start a new plot'''
        self.ncolor = nextColor() # make color iterator
        try:
            self.f.clf()  # clear the existing figure
        except:
            self.f = figure()# start new figure
        self.ax = self.f.add_subplot(111)
        self.has_labels = 0
        self.legend = None
        
        self.xmin = 1.0E99
        self.xmax = -1.0E99
        self.ymin = 1.0E99
        self.ymax = -1.0E99
        
        if self.force_linear_y:
            self.ax.set_yscale( 'Linear' )
        else:
            self.ax.set_yscale( self.plotOptionD['YAxis'] )
        self.ax.set_xscale( self.plotOptionD['XAxis'] )
        
        axisFormatter = FormatStrFormatter('%g')
        
        if  self.plotOptionD['XAxis']=='Log':
            logFormatter = FormatStrFormatter('%g')
            if self.plotOptionD['XMinorTicks']=='yes':
                self.ax.xaxis.set_minor_formatter(logFormatter)
        self.ax.xaxis.set_major_formatter(axisFormatter)
        
        if  (self.plotOptionD['YAxis']=='Log') and (not self.force_linear_y):
            logFormatter = FormatStrFormatter('%g')
            if  self.plotOptionD['YMinorTicks']=='yes':
                self.ax.yaxis.set_minor_formatter(logFormatter)
        self.ax.yaxis.set_major_formatter(axisFormatter)


        
    def add_curve(self, xL, yL, label='', show_pts=1, show_line=1, linewidth=2, color=None,
        markersize=10, integFill=None, marker='o', linetype='-', marker_alpha=1.0):
        
        if color is None:
            mfc=next(self.ncolor)
        else:
            mfc = color
            
            
        if label:
            self.has_labels = 1
        if show_pts and show_line:
            plot(xL,yL,'%s%s'%(linetype,marker) ,mfc=mfc,color=mfc, linewidth=linewidth,label=label, 
                markersize=markersize, alpha=marker_alpha)
        elif show_pts:
            if marker=='|':
                marker = (list( zip([-.05,.05,.05,-.05,-.05], [-1.,-1.,1.,1.,-1.]) ), 0)
                mfc = 'black'
                #marker_alpha = marker_alpha / 2.0
                markersize = old_div(markersize, 2.0)
            plot(xL,yL,mfc=mfc,color=mfc, linewidth=0,label=label, markersize=markersize, 
                alpha=marker_alpha, marker=marker)
        else:
            plot(xL,yL, linetype,mfc=mfc,color=mfc, linewidth=linewidth,label=label)
            
        if integFill:
            xPlotArr, yPlotArr = integFill
            fill_between(xPlotArr, [0.0]*len(xPlotArr), yPlotArr, facecolor='cyan', alpha=0.5, label='Area')
            
        self.xmin = min(self.xmin, min(xL))
        self.xmax = max(self.xmax, max(xL))
        self.ymin = min(self.ymin, min(yL))
        self.ymax = max(self.ymax, max(yL))
        
            
    
    def final_touches(self, title_str='', show_grid=True, show_legend=True, sigFontSize = 10,
        xaxis_str='x', yaxis_str='y'):
        
        if title_str:
            title( title_str )
            
        if xaxis_str:
            xlabel( xaxis_str )
            
        if yaxis_str:
            ylabel( yaxis_str )
        
        self.dx = 1.0
        self.dy = 1.0
        if self.xmin < 1.0E98:
            self.dx = old_div((self.xmax - self.xmin),20.0)
            xlim(self.xmin-self.dx, self.xmax+self.dx)
            self.dy = old_div((self.ymax - self.ymin),20.0)
            ylim(self.ymin-self.dy, self.ymax+self.dy)
        self.xmid = old_div((self.xmin+self.xmax),2.0)
        self.ymid = old_div((self.ymin+self.ymax),2.0)
            
            
        self.f.text(0.99, 0.02, ' ' + time.strftime('%m/%d/%Y'),
            horizontalalignment='right',verticalalignment='bottom', fontsize=sigFontSize)
        
        self.f.text(0.02, 0.02, "XYmath",
            horizontalalignment='left',verticalalignment='bottom', fontsize=sigFontSize)
            
        if show_legend and self.has_labels:
            #self.legendend(loc='best')
            #legend(loc='lower center',prop={'size':14})
            if self.plotOptionD['Legend Font Size']:
                propD = {'size':int(self.plotOptionD['Legend Font Size'])}
                self.legend = legend(loc=self.plotOptionD['Legend Location'], fancybox=True, prop=propD)
            else:
                self.legend = legend(loc=self.plotOptionD['Legend Location'], fancybox=True)
                
            alpha = float( self.plotOptionD['Legend Opacity'] )
            self.legend.get_frame().set_alpha(alpha)
            
            # tranformations to help convert pixels to other units
            #fromPixelToFig = self.f.transFigure.inverted()
            #fromPixelToData = self.ax.transData.inverted()
            #print ' get_bbox_to_anchor()=',self.legend.get_bbox_to_anchor()
            #print
            #print ' loc=',self.legend.get_window_extent()
            #print
            #print dir(self.legend.get_frame())
            #print 'bbox=',self.legend.get_frame().get_x()
            #bbox = self.legend.get_bbox_to_anchor()
            #print '(bbox.x0, bbox.y0) =',(bbox.x0, bbox.y0)
            #print '(bbox.x1, bbox.y1) =',(bbox.x1, bbox.y1)
            #print ' data units',fromPixelToData.transform((bbox.x1, bbox.y1))
            
        
        grid( show_grid )
        if show_grid:
            if  self.plotOptionD['XAxis']=='Log':# and self.plotOptionD['XMinorTicks']=='yes':
                self.ax.xaxis.grid(True, which='minor')

            if  (self.plotOptionD['YAxis']=='Log') and (not self.force_linear_y):# and self.plotOptionD['YMinorTicks']=='yes':
                self.ax.yaxis.grid(True, which='minor')


    def show_it(self):

        if hasattr(self, 'toolbar'):
            self.toolbar.pack_forget()
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
        
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame3)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.show()
        #self.canvas.draw()

        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.frame4 )
        self.toolbar.update()
        self.toolbar.pack()#side=TOP, fill=BOTH, expand=1)
        
        if hasattr(self.guiWin, 'tab_frames'):
            self.guiWin.tab_frames.ReConfigure(None)
            #self.guiWin.tab_frames.activeTab.event_generate('<Enter>', x=0, y=0)
            #self.guiWin.tab_frames.activeTab.event_generate('<Button-1>', x=0, y=0)
            #self.guiWin.tab_frames.activeTab.event_generate('<ButtonRelease-1>', x=0, y=0)
            #self.put_plot_on_clipboard()
    
    def clearAll(self):
        
        for k,i in list(self.children.items()):
            i.destroy()
            

    def put_plot_on_clipboard(self):
        def send_to_clipboard(clip_type, data):
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(clip_type, data)
            win32clipboard.CloseClipboard()
    
        w = int(self.frame3.winfo_width())
        h = int(self.frame3.winfo_height())
        
        print('w=%s, h=%s'%(w,h))
        if w>10 and h>10:
            iofile = io.BytesIO()
            
            self.toolbar.canvas.print_figure( iofile )
            iofile.seek(0)
            img = Image.open( iofile )
            #iofile.close() not req'd, closed by PIL
            
            iofile = io.BytesIO() # reinitialize
            img.convert("RGB").save(iofile, "BMP")
            data = iofile.getvalue()[14:]
            iofile.close()
            
            send_to_clipboard(win32clipboard.CF_DIB, data)
        
import tkinter

class DummyObject(object):
    pass


class _Testdialog(object):
    def __init__(self, master):
        frame = Frame(master, width=300, height=300)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        self.pageD = {}
        self.pageD['Plot'] = DummyObject()
        plotOptionD = {}
        plotOptionD['XAxis'] = 'Linear'
        plotOptionD['YAxis'] = 'Linear'
        plotOptionD['ShowTitle'] = 'yes'
        plotOptionD['ShowGrid'] = 'yes'
        plotOptionD['ShowLegend'] = 'yes'
        plotOptionD['Weights'] = 'no'
        plotOptionD['ShowPoints'] = 'yes'
        plotOptionD['FatLines'] = 'yes'
        plotOptionD['Legend Font Size'] = '14'
        plotOptionD['Legend Location'] = 'best'
        plotOptionD['Legend Opacity'] = '0.5'
        self.pageD['Plot'].plotOptionD = plotOptionD
        
        
        
        self.pageD['Plot'].pointStyleD =  {'circle':'o','square':'s','star':'*',
            'triangle':'^','diamond':'D','octagon':'8','pentagon':'p','hexagon':'H'}

        
        self.Button_1 = tkinter.Button(text="Test Plot Window", relief="raised", width="15")
        self.Button_1.place(x=84, y=36)
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    def Button_1_Click(self, event): #click method for component ID=1
        PlotWin = PlotWindow(self.master, self)

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
        
