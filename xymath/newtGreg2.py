from __future__ import absolute_import
from __future__ import division
from builtins import zip
from builtins import map
from builtins import range
from builtins import object
from past.utils import old_div

import bisect
        
class quadNG(object):  # quadratic Newton-Gregory Interpolation
    
    ''' quadratic Newton-Gregory Interpolation 
       assume a formula of:
    
       f = a + b(x-x0) + c(x-x0)(x-x1)
    '''
    
    def __init__(self, xInp, yInp):
        
        # make sure that x values are monotonically increasing
        x = list(map(float, xInp))
        y = list(map(float, yInp))
        c = list(zip(x,y))
        c.sort()
        x = []
        y = []
        aLast = None
        for aa,bb in c:
            # simply drop multivalued x points
            if aa != aLast:
                x.append(aa)
                y.append(bb)
            aLast = aa
        
        self.x = x
        self.y = y
        
        # start making quadratic constant arrays from difference tables
        self.a = []
        self.b = []
        self.c = []
            
        dif1 = []
        for i in range( len(x) - 1 ):
            dif1.append( old_div((y[i+1]-y[i]), (x[i+1]-x[i])) )

        dif2 = []
        for i in range( len(x) - 2 ):
            dif2.append( old_div((dif1[i+1]-dif1[i]), (x[i+2]-x[i])) )

        for i in range( len(x)-2):
            self.a.append( y[i] )
            self.b.append( dif1[i] )
            self.c.append( dif2[i] )


        self.iMax = len(self.a) - 1
        
    def __call__(self, xval=0.0):
        return self.getValue( xval )
        
    def getIndex(self, xval=0.0):
        '''Override this for computed index version'''
        
        i = bisect.bisect_left(self.x, xval) - 1
        
        if i<0:
            return 0
        elif i>self.iMax:
            return self.iMax

        return i
        
    def getValue(self, xval=0.0):
        xval = float( xval )
        
        if xval > self.x[-1]:
            return self.y[-1]
        
        if xval < self.x[0]:
            return self.y[0]
        
        i = self.getIndex(xval)
        dx = xval - self.x[i]
        dx2 = xval-self.x[i+1]
        return self.a[i] + dx*( self.b[i] + dx2*self.c[i] ) 
        
    def deriv(self, xval=0.0):
        xval = float( xval )
        i = self.getIndex(xval)
        dx = xval - self.x[i]
        dx2 = xval-self.x[i+1]
        return  self.b[i] + self.c[i]*(2.*xval - self.x[i] - self.x[i+1])
        
    def deriv2nd(self, xval=0.0):
        xval = float( xval )
        i = self.getIndex(xval)
        return 2.0*self.c[i] 
        
class quadNG_compInd(quadNG):  # quadratic Newton-Gregory Interpolation
    
    ''' quadratic Newton-Gregory Interpolation WITH Computed Index
       assume a formula of:
    
       f = a + b(x-x0) + c(x-x0)(x-x1)
    '''
    
    def __init__(self, xBeg, xEnd, yInp):
        '''Assume that yInp is in order.
           Create x array to correspond
        '''
        
        self.Npts = len(yInp)
        self.Nintervals = self.Npts-1
        self.h = old_div((xEnd-xBeg), float( self.Nintervals )) # constant step size
        
        self.xBeg = xBeg
        self.xEnd = xEnd
        
        xL = []
        for i in range( self.Nintervals ):
            xval = xBeg + float(i) * self.h
            xL.append( xval )
        xL.append( xEnd )
        
        quadNG.__init__(self, xL, yInp)
        
        self.iMax = len(self.a)-1

        
    def getIndex(self, xval=0.0):
        '''Overrides parent object to compute index
        
           Assume that the computation below is faster than bisect.bisect_left
           (Becomes more important for longer lists)
           profiling for lists of about 200 entries was about 20% faster
        '''
        
        i = int(  old_div((xval-self.xBeg), self.h)  )
        
        if i<0:
            return 0
        elif i>self.iMax:
            return self.iMax

        return i

if __name__ == "__main__": #Self Test
    
    import sys
    # do rapid laser example from PPT file
    x = [2.,4.25,5.25,7.81,9.2,10.6]
    y = [7.2,7.1,6.,5.,3.5,5.]
    
    if 1:
        q = quadNG_compInd(2.0, 10.6, y)
    else:
        q = quadNG( x, y)
    

    rs = [ ['x','f(x)cubic','fd1(x)','fd2(x)'] ]
    Npts = 100
    for i in range(Npts+1):
        xval = 12.*i/Npts
        rs.append( [xval, q(xval), q.deriv(xval), q.deriv2nd(xval)] )
    

    from . import xlChart
    xl = xlChart.xlChart()

    xl.xlApp.DisplayAlerts = 0  # Allow Quick Close without Save Message

    # Chart 1 / Sheet 1
    xl.makeChart(rs, title="Rapid Laser Data",nCurves = 3,
                 chartName="quadNG",
                 sheetName="quadNGData")

    rs = [ ['x','y'] ]
    for i in range(len(q.x)):
        rs.append( [q.x[i], q.y[i]] )

    xl.makeDataSheet( rs, sheetName="DataSheet")
    xl.addNewSeriesToCurrentSheetChart( xColumn=1, yColumn=2)
    xl.setMarkerSize( NSeries=4, size=10)
    xl.setSeriesColor( NSeries=4, red=255, green=0, blue=0)
    xl.setLineThickness( NSeries=4, thickness=0)
    xl.focusChart(1)

    sys.exit()
    
    
