#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
NonLinCurveFit fits a DataSet object to a non-linear function of x.

Uses the scipy.optimize.leastsq method to do a least squares curve fit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import object
from past.utils import old_div

import re
from numpy import dot, std, array, double, isfinite, corrcoef, ones, linspace, logspace, log10, column_stack
from numpy import absolute, zeros, pi, isnan
from scipy.optimize import leastsq
import numexpr
from .helper_funcs import bestFloatStr, INFINITY, fortran_doubleStr

from .eqn_parse import get_const_list
 
class NonLinCurveFit(object):
    """NonLinCurveFit fits a DataSet object to a non-linear functions of x."""

    @property
    def name(self):
        return self.get_eqn_str_w_consts()

    def __init__(self, ds, rhs_eqnStr='A*x**b',  fit_best_pcent=1,
        constDinp=None, ftol=1.49012e-08, xtol=1.49012e-08): # if constDinp, then use const values as initial values
        """Inits and fits DataSet, ds, to...
           y = rhs_eqnStr = f(x)
           where: rhs_eqnStr can have any constant names desired. A, b, theta
                  pi is recognized as the number 3.14159...
                  standard functions are recognized: sin, cos, tan, sqrt, exp, log, log10
                  x must be in the equation and is considered to be a numpy array of double
        """
        
        self.rhs_eqnStr = rhs_eqnStr # right hand side of eqn "y = rhs_eqnStr"
        self.fit_best_pcent = fit_best_pcent
        self._xymath_type = 'nonlinfit'
        
        self.ftol = ftol # tolerances in leastsq
        self.xtol = xtol
        
        self.ds = ds # DataSet object
        self.dsTimeStamp = None # set to self.ds.timeStamp in calc_std_values_from_cArr
        if constDinp:
            self.constD = constDinp
        else:
            self.constD = {}
        
        self.corrcoef = 0.0
        self.std = None
        self.pcent_std = None
        
        self.eqn_has_an_x = False # special handling for no x included
        
        self.tokenD, self.functionD, self.errorStr = get_const_list( rhs_eqnStr=rhs_eqnStr )
        
        if 'y' in self.tokenD:
            self.errorStr += '\nEquation must NOT contain a "y".'
        
        # ONLY continue if there is no errorStr
        if not self.errorStr:
            # put constants in equation into self.constD for use by numexpr
            for cname in list(self.tokenD.keys()):
                if cname in ['pi','x']:
                    if cname=='x':
                        self.eqn_has_an_x = True
                    pass # handle these later
                else:
                    if cname not in self.constD:
                        self.constD[cname] = 1.0
                        
            self.orderedConstL = list(self.constD.keys())
            self.orderedConstL.sort(key=str.lower) # put in alphabetical order
            
            self.fit_to_data()
    
    def fit_to_data(self):
        cL = []
        for c in self.orderedConstL:
            cL.append( self.constD[c] )
        #cArr = array(cL, dtype=double)
        
        ansArr = leastsq(self.residuals, cL, ftol=self.ftol, xtol=self.xtol)
        #print 'ansArr =',ansArr
        for i,c in enumerate(self.orderedConstL):
            self.constD[c] = ansArr[0][i]
        #print 'ans self.constD =',self.constD
        
        self.calc_std_values()
    
    def residuals(self, cArr):
        for i,c in enumerate(self.orderedConstL):
            self.constD[c] = cArr[i]
        
        if not self.ds.wtArr is None:
            if self.fit_best_pcent:
                return self.ds.wtArr*(self.ds.yArr - self.eval_xrange( self.ds.xArr )) / self.ds.yPcentDivArr
            else:
                return self.ds.wtArr*(self.ds.yArr - self.eval_xrange( self.ds.xArr ))
        else:
            if self.fit_best_pcent:
                return old_div((self.ds.yArr - self.eval_xrange( self.ds.xArr )), self.ds.yPcentDivArr)
            else:
                return self.ds.yArr - self.eval_xrange( self.ds.xArr )

    def eval_xrange(self, xArr ):# assume that equation startswith "y = " 
        
        if 'x' not in self.tokenD: # trick numexpr if there's no x in eqn
            cD = {'x':zeros(len(xArr)), 'pi':pi} # dictionary for evaluation
            for key,value in list(self.constD.items()): # build local_dict to execute numexpr in
                cD[key] = value
            #print 'in eval:',cD
            return numexpr.evaluate( self.rhs_eqnStr+'+x', local_dict=cD ) # add zeros via dummy "x"
        else:
            cD = {'x':xArr, 'pi':pi} # dictionary for evaluation
            for key,value in list(self.constD.items()): # build local_dict to execute numexpr in
                cD[key] = value
            #print 'in eval:',cD
            return numexpr.evaluate( self.rhs_eqnStr, local_dict=cD )
        

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


    def calc_std_values(self):
        
        # First set NonLinCurveFit timeStamp to ds.timeStamp
        self.dsTimeStamp = self.ds.timeStamp
        try:
            self.yCalcArr = self.eval_xrange( self.ds.xArr )
            #print 'self.yCalcArr=',self.yCalcArr
            
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

    def get_eqn_str_w_consts(self):
        return 'y = ' + self.rhs_eqnStr

    def get_fortran_eqn_str_w_numbs(self):
        s = ' ' + self.rhs_eqnStr + ' ' # make word boundaries apparent
        for c,val in list(self.constD.items()):
            val = fortran_doubleStr( val ) # convert to FORTRAN double precision literal
            s = re.sub(r'\b%s\b'%c, '%s'%val, s)
        
        s = s.replace('+ -','- ')
        return 'y = ' +s.strip()


    def get_eqn_str_w_numbs(self):
        s = ' ' + self.rhs_eqnStr + ' ' # make word boundaries apparent
        for c,val in list(self.constD.items()):
            s = re.sub(r'\b%s\b'%c, '%s'%val, s)
        
        s = s.replace('+ -','- ')
        return 'y = ' +s.strip()

    def get_full_description(self):
        """Returns a full summary of NonLinCurveFit."""
        
        sL = [self.get_eqn_str_w_consts()]
        for i,c in enumerate( self.orderedConstL ):
            sL.append('    %s = %s'%(c, bestFloatStr( self.constD[c] ) ) )
        
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
    yArr = array( [5,14.14,25.98,40,55.9,73.485], dtype=double) # 5 * x ** 1.5
    DS = DataSet(xArr, yArr, xName='fiddle', yName='faddle')
    
    #constDinp = {'A':1.0, 'b':1.0}
    C = NonLinCurveFit(DS, rhs_eqnStr='A*x**b')#, constDinp=constDinp)
    
    print(C.eval_xrange( xArr ) - yArr)
    print()
    print(C.get_full_description())
    #C.fit_to_data()
    #print C.get_full_description()
