from __future__ import absolute_import
from __future__ import division
from builtins import zip
from builtins import map
from builtins import range
from builtins import object
from past.utils import old_div

import bisect
        
class cubicNG(object):  # cubic Newton-Gregory Interpolation
    
    ''' cubic Newton-Gregory Interpolation 
       assume a formula of:
    
       f = a + b(x-x0) + c(x-x0)(x-x1) + d(x-x0)(x-x1)(x-x2)
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
        
        # start making cubic constant arrays from difference tables
        self.a = []
        self.b = []
        self.c = []
        self.d = []
            
        dif1 = []
        for i in range( len(x) - 1 ):
            dif1.append( old_div((y[i+1]-y[i]), (x[i+1]-x[i])) )

        dif2 = []
        for i in range( len(x) - 2 ):
            dif2.append( old_div((dif1[i+1]-dif1[i]), (x[i+2]-x[i])) )

        dif3 = []
        for i in range( len(x) - 3 ):
            dif3.append( old_div((dif2[i+1]-dif2[i]), (x[i+3]-x[i])) )

        for i in range( len(x)-3):
            self.a.append( y[i] )
            self.b.append( dif1[i] )
            self.c.append( dif2[i] )
            self.d.append( dif3[i] )

        self.iMax = len(self.a) - 1
        
    def __call__(self, xval=0.0):
        return self.getValue( xval )
        
    def getIndex(self, xval=0.0):
        '''Override this for computed index version'''
        
        i = bisect.bisect_left(self.x, xval) -2
        
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
        dx3 = xval-self.x[i+2]
        
        return self.a[i] + dx*( self.b[i] + dx2*(self.c[i] + dx3*self.d[i]) ) 
        
    def deriv(self, xval=0.0):
        xval = float( xval )
        i = self.getIndex(xval)
        x0 = self.x[i]
        x1 = self.x[i+1]
        x2 = self.x[i+2]
        return  self.b[i] + self.c[i]*(2.*xval - x0 - x1) \
            + self.d[i]*(3.*xval**2 - 2.*xval*(x0+x1+x2) + (x0*x1+x0*x2+x1*x2))
        
    def deriv2nd(self, xval=0.0):
        xval = float( xval )
        i = self.getIndex(xval)
        x0 = self.x[i]
        x1 = self.x[i+1]
        x2 = self.x[i+2]
        return 2.0*self.c[i] + self.d[i]*(6.*xval - 2.*(x0+x1+x2) )
        
class cubicNG_compInd(cubicNG):  # cubic Newton-Gregory Interpolation
    
    ''' cubic Newton-Gregory Interpolation WITH Computed Index
       assume a formula of:
    
       f = a + b(x-x0) + c(x-x0)(x-x1) + d(x-x0)(x-x1)(x-x2)
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
        
        cubicNG.__init__(self, xL, yInp)
        
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
    
    if 0:
        q = cubicNG_compInd(2.0, 10.6, y)
    else:
        q = cubicNG( x, y)
    

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
                 chartName="cubicNG",
                 sheetName="cubicNGData")

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
    
    
