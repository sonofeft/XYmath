#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
LinCurveFit fits a DataSet object to a linear sum of functions in x.

Uses the scipy.linalg.lstsq method to do a least squares curve fit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import object
from past.utils import old_div

#
# import statements here. (built-in first, then 3rd party, then yours)
from numpy import dot, std, array, double, isfinite, corrcoef, ones, linspace, logspace, log10, column_stack
from numpy import absolute, zeros, isnan, ma
from scipy import linalg
from scipy.optimize import leastsq
import numexpr

from .helper_funcs import bestFloatStr, INFINITY, fortran_doubleStr

inverseD = {'y':'y', '1/y':'1/(y)', 'log(y)':'exp(y)', 'exp(y)':'log(y)', 
    'log(1/y)':'1/exp(y)', 'exp(1/y)':'1/log(y)', 
        '1/log(y)':'exp(1/(y))', '1/exp(y)':'log(1/(y))',
        'y**2':'(y)**0.5', 'y**3':'(y)**(1./3.)', 'y**4':'(y)**0.25'}


def un_transform_y( y, ytran ):
    
    if ytran=='y':
        return y
    else:
        return numexpr.evaluate( inverseD[ytran] )

def eval_xrange( cArr, xArr, eqnStr ):# assume that eqnStr startswith "y = " 
    # make special case for constant-only
    if 'x' not in eqnStr and 'c0' in eqnStr:
        return cArr[0] * ones(len(xArr))
    s = eqnStr[4:]
    cD = {'x':xArr} # dictionary for c0, c1, etc.
    for i,c in enumerate(cArr): # build local_dict to execute numexpr in
        cD['c%i'%i] = cArr[i]
        
    #if '/x'in eqnStr and ma.masked_equal(xArr, 0.0).any():
    #    print 'Divide by Zero Warning...'
    #    print 'evaluating s=',s
    #    print 'eval=',numexpr.evaluate( s, local_dict=cD )
        
    return numexpr.evaluate( s, local_dict=cD )

class LinCurveFit(object):
    """LinCurveFit fits a DataSet object to a linear sum of functions in x."""

    @property
    def name(self):
        return self.get_eqn_str_w_consts()

    def eval_xrange(self, xPlotArr):
        return eval_xrange( self.cArr, xPlotArr, self.get_eqn_str_w_consts() )

    def __init__(self, ds, xtranL=None, ytran='y', fit_best_pcent=1,# e.g. ['const', 'x', 'x**2']       
        cArrInp=None): # if cArrInp, then skip cArr calc and jump straight to std calc
        """Inits and fits DataSet, ds, to xtranL"""
        
        self.fit_best_pcent = fit_best_pcent
        self._xymath_type = 'linfit'
        
        self.ds = ds # DataSet object
        self.dsTimeStamp = None # set to self.ds.timeStamp in calc_std_values_from_cArr
        self.xtranL = xtranL # list of x transformations
        self.ytran = ytran # can be 'y', '1/y', 'log(y)', etc.
        
        self.eqn_str_w_consts = None
        self.eqn_str_w_numbs = None
        self.corrcoef = 0.0
        self.std = None
        self.pcent_std = None
        
        # ONLY calc cArr if it is not input
        if cArrInp is None: # if constants are input, simply use them
            # First make good estimate of solution using matrix methods
            try:
                if self.fit_best_pcent:
                    #print 'Getting A,y for pcent_std, xtranL, ytran=',xtranL, ytran
                    A,y = ds.get_pcent_std_A_matrix( xtranL, ytran )
                else:
                    #print 'Getting A,y for std, xtranL, ytran=',xtranL, ytran
                    A,y = ds.get_A_matrix( xtranL, ytran )
                
                #print 'A=\n',A 
                #print 'y=',y
                self.cArr, resid, rank, sArr = linalg.lstsq(A, y)
                    
            except:
                self.cArr = ones( len(xtranL) )

            #print 'ds.wtArr=, ytran=',(ds.wtArr, ytran)
            #print "ytran!='y'",ytran!='y'
            #print "ds.wtArr is None",ds.wtArr is None
            
            # To stay true to selection of "Total Error" or "Percent Error"
            #    need to tweek matrix answer via leastsq approach.
            # Using good estimate of cArr from above, now use optimize leastsq
            if (not ds.wtArr is None) or ytran!='y':
                # After using matrix methods to estimate constants, use optimize.leastsq
                X = column_stack([ self.ds.getTransXArr(name) for name in self.xtranL ])
                        
                def ss_func( cArr ):
                    ytranArr = dot( X, cArr )
                    yCalcArr = un_transform_y( ytranArr, self.ytran )
                    
                    if not self.ds.wtArr is None:
                        #print 'Doing Linear fit with wtArr'
                        if  fit_best_pcent:
                            return self.ds.wtArr * (yCalcArr - self.ds.yArr)/self.ds.yPcentDivArr
                        else:
                            return self.ds.wtArr * (yCalcArr - self.ds.yArr)
                    else:
                        if  fit_best_pcent:
                            return old_div((yCalcArr - self.ds.yArr),self.ds.yPcentDivArr)
                        else:
                            return yCalcArr - self.ds.yArr
                
                #print 'self.cArr Before =',self.cArr
                #print '          Before std=',self.std,'  pcent_std=',self.pcent_std
                minResult = leastsq( ss_func, self.cArr)
                #print 'minResult =',minResult
                
                self.cArr = minResult[0]
        else:
            self.cArr = array(cArrInp, dtype=double)

        self.calc_std_values_from_cArr()
    
            
    def calc_std_values_from_cArr(self):
        if self.dsTimeStamp == self.ds.timeStamp:
            print('std and pcent_std left unchanged')
            return
        
        # First set LinCurveFit timeStamp to ds.timeStamp
        self.dsTimeStamp = self.ds.timeStamp
        self.corrcoef = 0.0 # in case it bombs show zero
        try:
            # if y is transformed, must un_transform_y
            X = column_stack([ self.ds.getTransXArr(name) for name in self.xtranL ])
            ytranArr = dot( X, self.cArr )
            self.yCalcArr = un_transform_y( ytranArr, self.ytran )
            #if self.fit_best_pcent:
            #    self.yCalcArr *= ds.yArr
            
            self.corrcoef = corrcoef(self.yCalcArr, self.ds.yArr)[0][-1]
            if isnan(self.corrcoef):
                self.corrcoef = 0.0
            
            errArr = self.ds.yArr - self.yCalcArr
            
            self.std = std( errArr ) # Calc standard deviation
        except:
            self.std = INFINITY
        
        try:
            self.pcent_std = 100.0 * std( old_div(errArr,self.ds.yPcentDivArr) )
            if not isfinite( self.pcent_std ):
                self.pcent_std = INFINITY
        except:
            self.pcent_std = INFINITY

    def get_x_plot_array(self, Npoints=100, logScale=0, xmin=None, xmax=None):
        
        if xmin is None:
            xmin = self.ds.xmin
        
        if xmax is None:
            xmax = self.ds.xmax
        
        if logScale:
            xPlotArr = logspace(log10(xmin), log10(xmax), num=Npoints)
        else:
            xPlotArr = linspace(xmin, xmax, num=Npoints)
        return xPlotArr

    def get_xy_plot_arrays(self, Npoints=100, logScale=0, xmin=None, xmax=None):
        xPlotArr = self.get_x_plot_array(Npoints=Npoints, logScale=logScale, 
            xmin=xmin, xmax=xmax)
        yPlotArr = self.eval_xrange( xPlotArr )
        return xPlotArr, yPlotArr
        
    def is_good_over_plot_range(self):
        '''Check for nan in plot range'''
        xPlotArr, yPlotArr = self.get_xy_plot_arrays()
        return not isnan(yPlotArr).any()

    def get_eqn_str_w_consts(self):
        if self.eqn_str_w_consts:
            return self.eqn_str_w_consts
        
        rhsL = []
        for i, xstr in enumerate( self.xtranL ):
            if '1/x' in xstr:
                rhsL.append( xstr.replace('1/x', 'c%i/x'%i) )
            else:
                rhsL.append( 'c%i*%s'%(i, xstr) )
        
        rhs = ' + '.join( rhsL )
        rhs = rhs.replace('*const','')
        
        invStr = inverseD[self.ytran]
        
        if '/y' in invStr:
            self.eqn_str_w_consts = 'y = ' + invStr.replace('y', '(%s)'%rhs)
        else:
            self.eqn_str_w_consts = 'y = ' + invStr.replace('y', rhs)
            
        #self.eqn_str_w_consts = self.eqn_str_w_consts.replace('**','^')
        return self.eqn_str_w_consts

    def get_eqn_str_w_numbs(self):
        if self.eqn_str_w_numbs:
            return self.eqn_str_w_numbs
        
        if not self.eqn_str_w_consts:
            self.get_eqn_str_w_consts()
            
        self.eqn_str_w_numbs = self.eqn_str_w_consts
        for i,c in enumerate( self.cArr ):
            starg = 'c%i'%i
            self.eqn_str_w_numbs = self.eqn_str_w_numbs.replace(starg, '%s'%self.cArr[i])
            
        self.eqn_str_w_numbs = self.eqn_str_w_numbs.replace(' + -',' - ')
        return self.eqn_str_w_numbs

    def get_fortran_eqn_str_w_numbs(self):
        if not self.eqn_str_w_consts:
            self.get_eqn_str_w_consts()
            
        self.eqn_str_w_numbs = self.eqn_str_w_consts
        for i,c in enumerate( self.cArr ):
            starg = 'c%i'%i
            self.eqn_str_w_numbs = self.eqn_str_w_numbs.replace(starg, fortran_doubleStr(self.cArr[i]))
            
        self.eqn_str_w_numbs = self.eqn_str_w_numbs.replace(' + -',' - ')
        return self.eqn_str_w_numbs

    def get_full_description(self):
        """Returns a full summary of LinCurveFit."""
        if not self.eqn_str_w_consts:
            self.get_eqn_str_w_consts()
        
        sL = [self.eqn_str_w_consts]
        for i,c in enumerate( self.cArr ):
            sL.append('    c%i = %s'%(i, bestFloatStr(c) ) )
        
        def get_desc( name, units ):
            if name:
                if units:
                    return '%s (%s)'%(name, units)
                else:
                    return name
            else:
                return units
                
        if self.ds.xName:
            sL.append('    x = %s'%get_desc(self.ds.xName, self.ds.xUnits) )
        if self.ds.yName:
            sL.append('    y = %s'%get_desc(self.ds.yName, self.ds.yUnits) )
        
        if isnan(self.corrcoef):
            sL.append('    Correlation Coefficient = Undefined' )
        else:
            sL.append('    Correlation Coefficient = %s'%bestFloatStr(self.corrcoef) )
        
        sL.append('    Standard Deviation = %s'%bestFloatStr(self.std) )
        sL.append('    Percent Standard Deviation = %s%%'%bestFloatStr(self.pcent_std) )
        sL.append('%s'%self.get_eqn_str_w_numbs() )
        
        return '\n'.join( sL )

if __name__=='__main__':
    from numpy import array, double
    from .dataset import DataSet
    
    xArr = array( [1,2,3,4,5,6], dtype=double)
    yArr = array( [10,5.49,0.89,-.14,-1.07,0.84], dtype=double)
    
    C = DataSet(xArr, yArr, xName='fiddle', yName='faddle')
    lf = LinCurveFit( C, ['const', 'x', 'x**2'])
    
    print(lf.get_full_description())
    print()
    #print "INFINITY =", bestFloatStr(INFINITY)
    print()
    
    
    lf2 = LinCurveFit( C, ['1/x', 'x'], ytran='1/y')
    
    print(lf2.get_full_description())
    print()
    
    #  y = 3.3888 + 0.3725*x
    xArr3 = array( [1, 3, 5, 7, 10, 12, 13, 16, 18, 20], dtype=double)
    yArr3 = array( [4, 5, 6, 5,  8,  7,  6,  9, 12, 11], dtype=double)
    C3 = DataSet(xArr3, yArr3, xName='LaDee', yName='Daa', xUnits='inches', yUnits='degF')
    lf3 = LinCurveFit( C3, ['const', 'x'])
    print(lf3.get_full_description())
    print()

