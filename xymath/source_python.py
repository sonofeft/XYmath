#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
Generate python code to perform the curve fit calculation from XYmath
"""
from __future__ import print_function
from __future__ import absolute_import

import time
from .eqn_parse import get_const_list

def make_fit_func_src( eqnObj ):
    '''Make python source code for LinCurveFit, NonLinCurveFit and Spline objects.'''

    # make comment string for any type of eqnObj
    full_desc = eqnObj.get_full_description()
    sL = ['    '+s for s in full_desc.split('\n')]
    sL.insert(0,'    Curve Fit Results from XYmath '+ time.strftime('%m/%d/%Y') )
    sL.insert(1,'    Can be called with x=float or x=numpy array\n')

        
    # build test evaluation
    if eqnObj.ds:
        x_test = eqnObj.ds.xArr[-1]
        data_comment = eqnObj.ds.get_data_pair_comment_lines(com_char='    ', len_max=80, sepChar=',')
        xmin = eqnObj.ds.xmin
        xmax = eqnObj.ds.xmax
    else:
        x_test = 1.0
        data_comment = ''
        xmin = 0.0
        xmax = 0.0


    if hasattr(eqnObj, 'get_eqn_str_w_numbs'):
        # Either LinCurveFit or NonLinCurveFit will work here
        
        # get any imports required from numpy module
        rhs_eqnStr = eqnObj.get_eqn_str_w_numbs()[4:]
        tokenD, functionD, errorStr = get_const_list( rhs_eqnStr=rhs_eqnStr )
        funcL = [s for s in functionD]
        for c in tokenD:
            if c=='pi':
                funcL.append( 'pi' )
        if funcL:
            numpy_imp = '\nfrom numpy import ' + ', '.join( funcL ) + '\n'
        else:
            numpy_imp = ''
        
        # setup string substitution dictionary
        substD = {'import':numpy_imp, 'func_name':'curve_fit_func', 'comment':'\n'.join(sL), 
                'rhs_eqnStr':rhs_eqnStr, 'x_test':x_test, 'y_xymath':eqnObj.eval_xrange(x_test), 
                'data_comment':data_comment, 'xmin':xmin, 'xmax':xmax}
            
        return func_src_template%substD
    
    else: # spline here
        # setup string substitution dictionary
        xL = [x for x in eqnObj.ds.xArr]
        yL = [y for y in eqnObj.ds.yArr]
        substD = {'func_name':'curve_fit_func', 'comment':'\n'.join(sL), 'order':eqnObj.order,
                'x_test':x_test, 'y_xymath':eqnObj.eval_xrange(x_test), 'xL':xL, 'yL':yL,
                'smoothing':eqnObj.smoothing, 'data_comment':data_comment, 'xmin':xmin, 'xmax':xmax}
            
        return spline_template%substD
#==========================================================================
spline_template = """#!/usr/bin/env python
# -*- coding: ascii -*-
# This Python Source Code Generated by XYmath

from scipy.interpolate import UnivariateSpline
from numpy import array, double

# make data arrays for spline to use
xArr = array( %(xL)s, dtype=double)
yArr = array( %(yL)s, dtype=double)

# make spline only once
s = UnivariateSpline(xArr, yArr, k=%(order)s, s=%(smoothing)s)

def %(func_name)s( x ):
    '''
%(comment)s

%(data_comment)s
    '''
    if x<%(xmin)s or x>%(xmax)s:
        print 'WARNING... x is outside range in %(func_name)s'
        print '  x =',x,' x range = (%(xmin)s to %(xmax)s)'
    
    return s( x )

if __name__=='__main__':
    print '='*44
    y_test = %(func_name)s( %(x_test)s )
    print 'y_test  =',y_test,'for x_test =',%(x_test)s
    print 'y_xymath=',%(y_xymath)s
    print
    print 'y_test should equal y_xymath above.'
"""
# ======================================================================
func_src_template = """#!/usr/bin/env python
# -*- coding: ascii -*-
# This Python Source Code Generated by XYmath
%(import)s
def %(func_name)s( x ):
    '''
%(comment)s

%(data_comment)s
    '''
    if x<%(xmin)s or x>%(xmax)s:
        print 'WARNING... x is outside range in %(func_name)s'
        print '  x =',x,' x range = (%(xmin)s to %(xmax)s)'
    
    return %(rhs_eqnStr)s

if __name__=='__main__':
    print '='*44
    y_test = %(func_name)s( %(x_test)s )
    print 'y_test  =',y_test,'for x_test =',%(x_test)s
    print 'y_xymath=',%(y_xymath)s
    print
    print 'y_test should equal y_xymath above.'
"""

if __name__=='__main__':
    from numpy import array, double
    from .dataset import DataSet
    from .linfit import LinCurveFit
    from .nonlinfit import NonLinCurveFit
    from .splines import Spline
    
    xArr = array( [1,2,3,4,5,6], dtype=double)
    yArr = array( [1.2,3.1,9.2,15.8,24.6,36.5], dtype=double)
    
    DS = DataSet(xArr, yArr, xName='fiddle', yName='faddle')
    lf = LinCurveFit( DS, ['const', 'x', 'x**2'])
    
    src = make_fit_func_src( lf )
    print(src)
    print('='*44)
    
    lf = LinCurveFit( DS, ['const', 'x'], ytran='log(y)')
    src = make_fit_func_src( lf )
    print(src)
    
    print('='*44)
    nlf = NonLinCurveFit(DS, rhs_eqnStr='A * exp(c*x/pi)')
    src = make_fit_func_src( nlf )
    print(src)
        
    print('='*44)
    nlf = NonLinCurveFit(DS, rhs_eqnStr='A * pi*x + c')
    src = make_fit_func_src( nlf )
    print(src)
        
    print('='*44, ' Spline')
    sp = Spline(DS, order=2, smoothing=0.0)
    src = make_fit_func_src( sp )
    print(src)
    