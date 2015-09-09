#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
XYmath fits curves to data sets and evaluates properties of those curves

<Paragraph description see docstrings at http://www.python.org/dev/peps/pep-0257/>

XYmath is a recreation of the code I wrote 20 years ago in pascal.

After fitting data, such operations as root finding, integration, and
derivative finding can be performed.

The code will also create documentation, plots, excel spreadsheets 
of the results.

An added feature is the generation of code (python or FORTRAN) functions 
to calculate the selected curve fits.

"""
from __future__ import print_function
from __future__ import division
from builtins import zip
from builtins import object
from past.utils import old_div

#
# import statements here. (built-in first, then 3rd party, then yours)
import sys
import time
from numpy import empty, ones, array, double, dot, column_stack, std, finfo, float64
from numpy import sqrt, all, sum, zeros, absolute, nonzero, append, lexsort
import numexpr

EPS_FLOAT = finfo(float64).eps

class DataSet(object):
    """XYmath fits curves to data sets and evaluates properties of those curves"""

    def __init__(self, xArr=array([1.,2.]), yArr=array([3.,4.]), wtArr=None, 
        xName='', yName='', xUnits='', yUnits='', timeStamp=None):
        self.xArr = array(xArr, dtype=double)
        self.yArr = array(yArr, dtype=double)
        
        if wtArr is None:
            self.wtArr = wtArr
        else:
            self.wtArr = array(wtArr, dtype=double)
        
        self.xName = xName
        self.yName = yName
        self.xUnits = xUnits
        self.yUnits = yUnits
        
        self.update_internal_vars()
        if timeStamp is None:
            self.timeStamp = time.time()
        else:
            self.timeStamp = timeStamp
            
            
    def update_internal_vars(self):
        '''When the dataset changes, some internal vars must change.'''
        self.timeStamp = time.time() # __init__ might override this
        
        self.transXArrD = {}
        self.transYArrD = {}
        self.N = len( self.yArr )
        
        #self.all_nonzero = all(self.yArr != 0.0)
        
        self.xmin = self.xArr.min()
        self.xmax = self.xArr.max()
        
        # make a yArr divisor for pcent_std in case there is a 0.0 in the yArr
        try:
            self.ymin_abs = absolute( self.yArr[nonzero(self.yArr)] ).min()
        except:
            self.ymin_abs = EPS_FLOAT
        #print 'self.ymin_abs=',self.ymin_abs
        self.yPcentDivArr = array( [v if v!=0.0 else self.ymin_abs for v in self.yArr] )
        #print 'self.yPcentDivArr =',self.yPcentDivArr

    def xy_arrays_wo_double_values(self):
        '''Anytime an x value is entered more than once, that x location can have two 
        different y values.  Replace those locations with the average y value.'''
        
        xD = {}
        yD = {}
        for x,y in zip(self.xArr, self.yArr):
            s = '%.7g'%x
            if s in xD:
                xD[s].append(x)
                yD[s].append(y)
            else:
                xD[s] = [x]
                yD[s] = [y]
        
        keyL = list(xD.keys())
        keyL.sort( key=float )
        xL = []
        yL = []
        for s in keyL:
            if len(xD[s])>1:
                xL.append( old_div(sum(xD[s]), float(len(xD[s]))) )
                yL.append( old_div(sum(yD[s]), float(len(yD[s]))) )
            else:
                xL.append( xD[s][0] )
                yL.append( yD[s][0] )
            
        #print 'xL=',xL
        #print 'yL=',yL
        return array(xL, dtype=double), array(yL, dtype=double)

    def sort_by_x(self):
        #print '---'
        #print 'xArr=',self.xArr
        #print 'yArr=',self.yArr
        if not self.wtArr is None:
            indL = lexsort( (self.wtArr, self.yArr, self.xArr) )# faster/smaller sorting last axis
            self.wtArr = self.wtArr[indL]
        else:
            indL = lexsort( (self.yArr, self.xArr) )# faster/smaller sorting last axis
        #print indL
        self.xArr = self.xArr[indL] # use fancy indexing to reorder data
        self.yArr = self.yArr[indL]
        #print 'xArr=',self.xArr
        #print 'yArr=',self.yArr
        
        # update_internal_vars, but preserve timeStamp
        ts = self.timeStamp
        self.update_internal_vars()
        self.timeStamp = ts

    def swap_x_and_y(self):
        self.xArr, self.yArr = self.yArr, self.xArr
        self.xName, self.yName = self.yName, self.xName
        self.xUnits, self.yUnits = self.yUnits, self.xUnits
        self.update_internal_vars()

    def replace_all_xy_data(self, xArr=array([1.,2.]), yArr=array([3.,4.]), wtArr=None):
        self.xArr = xArr
        self.yArr = yArr
        self.wtArr = wtArr
        self.update_internal_vars()

    def set_an_xy_pair(self, i=0, xval=1.0, yval=1.0):
        if i < self.N:
            self.xArr[i] = xval
            self.yArr[i] = yval
            self.update_internal_vars()
    
    def set_all_weights_to_one(self):
        self.wtArr = ones( self.N, dtype=double)
        self.update_internal_vars()

    def append_xy(self, xval=1.0, yval=1.0, wt=1.0 ):
        self.xArr = append( self.xArr, xval )
        self.yArr = append( self.yArr, yval )
        #if self.wtArr!=None:
        if not self.wtArr is None:
            self.wtArr = append( self.wtArr, wt )
        self.update_internal_vars()

    def append_xy_list(self, xvalL, yvalL, wtL=None ):
        self.xArr = append( self.xArr, xvalL )
        self.yArr = append( self.yArr, yvalL )
        #if self.wtArr!=None:
        if not self.wtArr is None:
            if wtL:
                self.wtArr = append( self.wtArr, wtL )
            else:
                self.wtArr = append( self.wtArr, ones( len(xvalL), dtype=double) )
        self.update_internal_vars()
        
    def get_x_desc(self):
        if self.xName:
            if self.xUnits:
                return '%s (%s)'%(self.xName, self.xUnits)
            else:
                return self.xName
        else:
            return self.xUnits
        
    def get_y_desc(self):
        if self.yName:
            if self.yUnits:
                return '%s (%s)'%(self.yName, self.yUnits)
            else:
                return self.yName
        else:
            return self.yUnits

    def getTransXArr(self, name='const'): # can be 'x', '1/x', etc.
        """Returns and perhaps creates/adds transformed xArr to transXArrD."""
        
        if name in self.transXArrD:
            return self.transXArrD[name]
        
        if name=='const':
            self.transXArrD[name] = ones( self.N, dtype=double)
            return self.transXArrD[name]
        
        # Don't bother with numexpr if just returning xArr
        if name=='x':
            self.transXArrD[name] = self.xArr
            return self.transXArrD[name]            
        
        # At this point, only transformations of x will occur
        x = self.xArr
        self.transXArrD[name] = numexpr.evaluate( name )
        return self.transXArrD[name]
        

    def getTransYArr(self, name='y'): # can be 'y', '1/y', etc.
        """Returns and perhaps creates/adds transformed yArr to transYArrD."""
        
        if name in self.transYArrD:
            return self.transYArrD[name]
        
        # Don't bother with numexpr if just returning yArr
        if name=='y':
            self.transYArrD[name] = self.yArr
            return self.transYArrD[name]            
        
        # At this point, only transformations of y will occur
        y = self.yArr
        self.transYArrD[name] = numexpr.evaluate( name )
        return self.transYArrD[name]
        
    
    def get_A_matrix(self, xtranL=None, ytran=None): # e.g. ['const', 'x', 'x**2'] and 'y' or '1/y'
        '''Get A matrix for fitting to "std".  Ignore wtArr for now.'''
        A = column_stack([ self.getTransXArr(name) for name in xtranL ])
        y = self.getTransYArr( ytran )
        return A,y
    
    def get_pcent_std_A_matrix(self, xtranL=None, ytran=None): # e.g. ['const', 'x', 'x**2'] and 'y' or '1/y' 
        '''Get A matrix for fitting to "pcent_std".  Ignore wtArr for now.'''
        A = column_stack([ old_div(self.getTransXArr(name),self.yPcentDivArr) for name in xtranL ])
        y = old_div(self.getTransYArr( ytran ),self.yPcentDivArr)
        return A,y
    
    def summary_print(self):
        print('N =',self.N)
        print('xArr =',self.xArr)
        print('yArr =',self.yArr)
        print('wtArr =',self.wtArr)
        print('xName =',self.xName)
        print('yName =',self.yName)
        print('xUnits =',self.xUnits)
        print('yUnits =',self.yUnits)
        print('timeStamp =',self.timeStamp)
        print('xmin =',self.xmin)
        print('xmax =',self.xmax)
        print('ymin_abs =',self.ymin_abs)
        print('yPcentDivArr=',self.yPcentDivArr)
        
    def get_data_pair_comment_lines(self, com_char='#', len_max=80, sepChar=','):
        '''Return dataset in a format consistent with a comment block'''
        
                
        if self.wtArr is None:
            src = '%s (x,y) Data Pairs from %s Used in Curve Fit '%\
                (com_char, time.strftime("%m/%d/%Y", time.localtime(self.timeStamp) ))
            
            sL = [src]
            
            src = '%s (x,y) = '%com_char
            for x,y in zip(self.xArr, self.yArr):
                s = '(%g,%g)'%(x,y)
                if len(src) + len(s) < len_max:
                    src += s + sepChar
                else:
                    sL.append( src )
                    src = com_char + '    ' + s + sepChar
            
            src = src[:-1] # get rid of trailing sepChar
            sL.append( src )
            return '\n'.join( sL ) + '\n'
        else:
            # Need to include weights
            src = '%s (x,y)*Wt Weighted Data Set from %s.(Only showing weights!=1.0)'%\
                (com_char, time.strftime("%m/%d/%Y", time.localtime(self.timeStamp) ))
        
            sL = [src]
            
            src = '%s (x,y)*Wt = '%com_char
            for x,y,w in zip(self.xArr, self.yArr, self.wtArr):
                if abs(1.0-w)>0.001:
                    s = '(%g,%g)*%g'%(x,y,w)
                else:
                    s = '(%g,%g)'%(x,y)
                if len(src) + len(s) < len_max:
                    src += s + sepChar
                else:
                    sL.append( src )
                    src = com_char + '    ' + s + sepChar
            
            src = src[:-1] # get rid of trailing sepChar
            sL.append( src )
            return '\n'.join( sL ) + '\n'
        

if __name__=='__main__':
    from scipy import linalg
    
    xArr = array( [1,2,3,4,5,6], dtype=double)
    yArr = array( [10,5.49,0.89,-.14,-1.07,0.84], dtype=double)
    
    C = DataSet(xArr, yArr)
    C.getTransXArr(name='const')
    C.getTransXArr(name='x')
    C.getTransXArr(name='1/x')
    C.getTransXArr(name='x**2')
    
    C.getTransYArr(name='y')
    C.getTransYArr(name='1/y')
    
    for item in list(C.transXArrD.items()):
        print(item)
    print()
    for item in list(C.transYArrD.items()):
        print(item)
    
    print()
    A,y = C.get_A_matrix( ['const', 'x', 'x**2'], 'y' )
    print('A =',A)
    
    cArr, resid, rank, sArr = linalg.lstsq(A, yArr)
    yCalcArr = dot( A, cArr )
    errArr = yArr - yCalcArr

    print('cArr=',['%g'%v for v in cArr])
    print('resid=', resid)
    print('rank=',rank)
    print('sArr=',['%g'%v for v in sArr])
    print('yCalcArr=',['%g'%v for v in yCalcArr])
    print('errArr=',['%g'%v for v in errArr])
    print('std=',std( errArr ), 'sqrt(resid/C.N)=',sqrt(old_div(resid,C.N)))
    
    print('='*66)
    C.replace_all_xy_data( xArr=array([2,7,1,4]), yArr=array([22.2,0.7,11.1,4.4]), wtArr=None)
    C.sort_by_x()
    
    
