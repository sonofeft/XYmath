#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
Math functions to support XYmath

Includes: Min/Max finding, root finding, integration over an interval, 
and numerical derivatives
"""
from __future__ import print_function
from __future__ import division
from builtins import range
from past.utils import old_div

from numpy import linspace, array, argmin, argmax 
from scipy import optimize, integrate, misc

def find_values_at_x(obj, xval, xlo=0.0, xhi=10.0, nhi=2):
    '''Find value of obj at val as well as derivatives. n=1 is 1st derivative, etc.'''
    
    dx = old_div((xhi-xlo), 1000.0) # make dx appropriate for range
    
    def f( xval ):
        return obj.eval_xrange( xval )
    
    resultL = [ float(f(xval)) ]
    for n in range(1, nhi+1):
        resultL.append( misc.derivative(f, xval, n=n, dx=dx) )
        
    return resultL

def find_integral(obj,  xlo=0.0, xhi=10.0):
    '''Find integral over x range.'''
    def f( xval ):
        return obj.eval_xrange( xval )
    
    integral, error = integrate.quad(f, xlo, xhi )
    return integral, error

def find_root(obj, ygoal=0.0, xlo=0.0, xhi=10.0):
    '''Find roots in x range.'''
    # first find a range that has a root
    xArr = linspace(xlo, xhi, 1000)
    yArr = obj.eval_xrange(xArr) - ygoal
    indexL = [] # index of a solution segment
    for i in range(1, len(xArr) ):
        if yArr[i-1]*yArr[i] <= 0.0:
            indexL.append(i)
    
    xrootL = [] # may be multiple roots
    def f( xval ):
        return obj.eval_xrange( xval ) - ygoal
    for i in indexL:            
        x_root = optimize.brentq(f, xArr[i-1], xArr[i])
        xrootL.append( x_root )
    
    xRootArr = array( xrootL )
    yRootArr = obj.eval_xrange( xRootArr )
    return xRootArr, yRootArr

def find_min_max(obj, xlo=0.0, xhi=10.0, xtol=1.0e-12):
    """Find Min/Max values over interval xlo to xhi"""

    # do a little brute force to keep away from local minima/maxima
    xArr = linspace(xlo, xhi, 1000)
    yArr = obj.eval_xrange(xArr)
    
    # find index of min and max y value in array over range
    imin = argmin( yArr )
    imax = argmax( yArr )
    print('imin=',imin,'imax=',imax)
    
    dx = old_div((xhi-xlo),990.0)
    
    xlo_min = max(xlo, xArr[imin]-dx)
    xhi_min = min(xhi, xArr[imin]+dx)
    
    xlo_max = max(xlo, xArr[imax]-dx)
    xhi_max = min(xhi, xArr[imax]+dx)

    def f( xval ):
        return -obj.eval_xrange( xval )
        
    x_max = optimize.fminbound(f, xlo_max, xhi_max, xtol=1e-12)
    
    def f2( xval ):
        return obj.eval_xrange( xval )
        
    x_min = optimize.fminbound(f2, xlo_min, xhi_min, xtol=1e-12)
    y_min = f2(x_min)
    y_max = f2(x_max)

    return x_min, y_min, x_max, y_max

if __name__=='__main__':
    pass

