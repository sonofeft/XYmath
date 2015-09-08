#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
Splines fits a DataSet object to a spline function in x, with or w/o smoothing.

Uses the scipy.interpolate.UnivariateSpline method to do spline fit.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import object
from past.utils import old_div

from scipy.interpolate import UnivariateSpline
from numpy import linspace, corrcoef, isfinite, std, isnan, logspace, log10
from xymath.helper_funcs import intCast, floatCast, INFINITY, bestFloatStr

splineNameD = { 1:"Linear Interpolation",
            2:"Quadratic Spline",
            3:"Cubic Spline", 
            4:"Quartic Spline",
            5:"Quintic Spline" } 
 
class Spline(object):
    """Spline object is order 1 to 5 spline fitted to dataset

    Longer class information....
    Longer class information....
    """

    def __init__(self, ds, order=1, smoothing=0.0):
        """Inits Spline with dataset, ds."""
        self.ds = ds
        self.dsTimeStamp = None # set to self.ds.timeStamp in calc_std_values_from_cArr
        self.corrcoef = 0.0
        self.std = None
        self.pcent_std = None
        
        self.order = min(5, max(1,intCast(order)))
        self.smoothing = max(0.0, floatCast(smoothing))
        self.name = splineNameD[order]
        if self.smoothing > 0.0:
            self.name = 'Smoothed ' + self.name + '(s=%g)'%self.smoothing
        
        xL, yL = ds.xy_arrays_wo_double_values()
        
        self.s = UnivariateSpline(xL, yL, k=self.order, s=self.smoothing)
        #self.s = UnivariateSpline(ds.xArr, ds.yArr, k=self.order, s=self.smoothing)
        self._xymath_type = 'spline'
        
        self.calc_std_values()
    
    def eval_xrange(self, xArr):
        """Returns y array for input x array (can also be a single x float value)."""
        return self.s( xArr )

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
        if self.dsTimeStamp == self.ds.timeStamp:
            print('std and pcent_std left unchanged')
            return
        
        # First set LinCurveFit timeStamp to ds.timeStamp
        self.dsTimeStamp = self.ds.timeStamp
        try:
            self.yCalcArr = self.eval_xrange( self.ds.xArr )
            
            self.corrcoef = corrcoef(self.yCalcArr, self.ds.yArr)[0][-1]
            
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
            
        #print 'Spline std=%s, pcent_std=%s, corrcoef=%s'%(self.std, self.pcent_std, self.corrcoef)

    def get_eqn_str_w_consts(self):
        return 'y = ' + self.name


    def get_full_description(self):
        """Returns a full summary of LinCurveFit."""
        
        sL = ['Spline Curve Fit of DataSet of Order=%s, Smoothing=%s'%(self.order, self.smoothing)]
        
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
        
        if self.smoothing > 0.0:
            if isnan(self.corrcoef):
                sL.append('    Correlation Coefficient = Undefined' )
            else:
                sL.append('    Correlation Coefficient = %s'%bestFloatStr(self.corrcoef) )
            
            sL.append('    Standard Deviation = %s'%bestFloatStr(self.std) )
            sL.append('    Percent Standard Deviation = %s%%'%bestFloatStr(self.pcent_std) )
        else:
            sL.append('    Unsmoothed spline goes through every data point.')
        
        
        return '\n'.join( sL )

if __name__=='__main__':
    C = Spline()
