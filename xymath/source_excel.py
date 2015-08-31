#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
Save into Excel the curve fit calculation from XYmath
"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import range

import time
import re
from .eqn_parse import get_const_list
from .xlChart import addColumnToRS, xlChart

def replace_word(eqnStr, s_old, s_new):
    s = ' ' + eqnStr + ' ' # make word boundaries apparent
    s = re.sub(r'\b%s\b'%s_old, s_new, s)
    return s[1:-1] # get rid of spaces added at step 1

def make_fit_excel( eqnObj ):
    '''Make python source code for LinCurveFit, NonLinCurveFit and Spline objects.'''

    # Don't bother if there's no dataset
    if not eqnObj.ds:
        return

    try:
        xl = xlChart()
    except:
        return False
        
    # build test evaluation
    rs_data = addColumnToRS(None, 'X Data', eqnObj.ds.xArr)
    rs_data = addColumnToRS(rs_data, 'Y Data', eqnObj.ds.yArr)
    
    xplotArr, yplotArr = eqnObj.get_xy_plot_arrays()
    rs_data = addColumnToRS(rs_data, 'X Range', xplotArr)

    if hasattr(eqnObj, 'get_eqn_str_w_numbs'):
        # Either LinCurveFit or NonLinCurveFit will work here
        
        # get any imports required from numpy module
        rhs_eqnStr = eqnObj.get_eqn_str_w_numbs()[4:]
        xl_eqnStr = rhs_eqnStr.replace( '**', '^')
        xl_eqnStr = replace_word(xl_eqnStr, 'pi', 'pi()')   # pi is func in Excel
        xl_eqnStr = "=" + replace_word(xl_eqnStr, 'log', 'ln')   # log is base 10 in Excel
        print('xl_eqnStr =',xl_eqnStr)
        
        irow = 2
        eL = []
        for i in range( len(xplotArr) ):
            cell = 'C%i'%(irow+i)
            s = replace_word(xl_eqnStr, 'x', cell)
            eL.append( s )
        rs_data = addColumnToRS(rs_data, 'Y Equation', eL)
    else:
        rs_data = addColumnToRS(rs_data, 'Y Fit', yplotArr)
        
    #print rs_data
    xl.makeChart(rs_data, nCurves = 1,
        title="XYmath Curve Fit Results\n%s"%eqnObj.get_eqn_str_w_consts(),
         chartName="XYmath Chart",
         sheetName="Dataset",
         yLabel=eqnObj.ds.get_y_desc(), xLabel=eqnObj.ds.get_x_desc())

    xl.addNewSeriesToCurrentSheetChart( xColumn=3, yColumn=4)
    
    xl.setLineStyle( NSeries=1, style=0)
    xl.setMarkerSize(NSeries=1, size=20)
    xl.turnMarkerOnOff( NSeries=2, showPoints=0)

    # make comment string for any type of eqnObj
    try:
        short_desc = eqnObj.get_eqn_str_w_numbs()
    except:
        short_desc = eqnObj.get_eqn_str_w_consts()
    full_desc = eqnObj.get_full_description()
    
    xl.addTextBox(short_desc)
    
    sL = ['    '+s for s in full_desc.split('\n')]
    sL.insert(0,'    Curve Fit Results from XYmath '+ time.strftime('%m/%d/%Y') )
    rs = addColumnToRS( None, '', sL )
    
    xl.setRangeOnCurrentSheet( rs, upperLeft='$F$3', bgColor=None)
    
    return True
    

if __name__=='__main__':
    from numpy import array, double
    from .dataset import DataSet
    from .linfit import LinCurveFit
    from .nonlinfit import NonLinCurveFit
    from .splines import Spline
    import sys
    
    xArr = array( [1,2,3,4,5,6], dtype=double)
    yArr = array( [1.2,3.1,9.2,15.8,24.6,36.5], dtype=double)
    
    DS = DataSet(xArr, yArr, xName='fiddle', yName='faddle')
    lf = LinCurveFit( DS, ['const', 'x', 'x**2'])
    
    src = make_fit_excel( lf )
    sys.exit()
    
    print(src)
    print('='*44)
    
    lf = LinCurveFit( DS, ['const', 'x'], ytran='log(y)')
    src = make_fit_excel( lf )
    print(src)
    
    print('='*44)
    nlf = NonLinCurveFit(DS, rhs_eqnStr='A * exp(c*x/pi)')
    src = make_fit_excel( nlf )
    print(src)
        
    print('='*44)
    nlf = NonLinCurveFit(DS, rhs_eqnStr='A * pi*x + c')
    src = make_fit_excel( nlf )
    print(src)
        
    print('='*44, ' Spline')
    sp = Spline(DS, order=2, smoothing=0.0)
    src = make_fit_excel( sp )
    print(src)
    