#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
this file contains helper functions for XYmath
"""
from __future__ import print_function
from __future__ import division
from builtins import str
from past.utils import old_div


#
# import statements here. (built-in first, then 3rd party, then yours)
#
from numpy import finfo

INFINITY = finfo('d').max

colorL = ['r','g','b','darkcyan','m','olive','deepskyblue','darkorange','brown',
    'deeppink','black','crimson','seagreen','fuchsia','darkviolet','coral','darkred','darkgreen','darkblue','c' ]


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


def about_equal(v1, v2, NdecPts=7):
    fmt = '%%.%ig'%NdecPts
    return fmt%v1==fmt%v2

def bestFloatStr(fval):
    """Make prettiest float."""
    return  str(fval)
    
    try:
        return  ('%g'%fval)
    except:
        return  str(fval)
                


def intCast( val=0 ):
    try:
        return int(val)
    except:
        return 0
        
def floatCast( val=0.0 ):
    try:
        return float(val)
    except:
        return 0.0

def is_number( nval ):
    
    if type(nval)==type(11) or type(nval)==type(1.234):
        return 1
    
    if type(nval)==type('string'):
        nval = nval.strip()
    
    try:
        if floatCast( nval) == float(nval):
            return 1
    except:
        pass
        
    return 0


def is_int( ival ):
    
    if type(ival)==type(11):
        return 1
    
    if type(ival)==type('string'):
        if ival.find('.')>=0:
            return 0
    
    try:
        if intCast( ival) == int(ival):
            return 1
    except:
        pass
        
    return 0

def is_float( fval ):
    
    if type(fval)==type(11.11):
        return 1
    
    if type(fval)==type('string'):
        if fval.find('.')==-1:
            return 0
    
    try:
        if floatCast( fval) == float(fval):
            return 1
    except:
        pass
        
    return 0

    
def fortran_doubleStr(sInp):
    '''Make input number into a double precision FORTRAN literal float'''
    s = str(sInp).strip().lower()
    
    if s.find('e')>=0:
        s = string.replace(s,'e','D')
    else:
        s = s + 'D0'
    return s

            

if __name__=='__main__':
    print()
    def call_best( val ):
        vStr = bestFloatStr(val)
        print('for %15s bestFloatStr=%s'%(val, vStr))
        
    call_best( 1.11000 )
    call_best( old_div(1.0,9.0) )
    call_best( 100.0 )
    call_best( 100 )
    call_best( '100x' )


