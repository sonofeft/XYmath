#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
Parse the right hand side of a user-defined equation y=f(x)
"""
from __future__ import print_function

import ast

import token
import traceback


legalFuncL = ['cosh',
    'tan','log','sqrt','log10','cos',
    'sinh','tanh','sin','exp','log1p']

fixedConstL = ['pi']

def get_const_list( rhs_eqnStr= "A*sin(B*x)*x**2"):
    errorStrL = [] # assume no error for now
    tokenD = {}
    functionD = {}
    errorStr = ''
    
    try:
        tree = ast.parse( rhs_eqnStr )
        for node in ast.walk(tree):
            if 'id' in node.__dict__:
                id = node.__dict__['id']

                if id in legalFuncL:
                    functionD[id] = id
                else:
                    tokenD[id] = id

    except:
        errorStrL = ['ERROR in Equation String']
        
        tbStr = traceback.format_exc() # get error message
        tbL = tbStr.split('\n')
        
        active = 0
        for line in tbL:
            if active:
                errorStrL.append( line )
            if line.find('''File "<string>"''')>=0:
                active = 1
        if not active:
            errorStrL = tbL[-4:] # next best guess at interesting part of message
                
        errorStrL.append('Please Correct Error and Try Again')
    if errorStrL:
        errorStr = '\n'.join(errorStrL)
    return tokenD, functionD, errorStr


if __name__=='__main__':
    
    tokenD, functionD, errorStr = get_const_list( rhs_eqnStr= "A*sin(B*pi*x)*x**2")
    print('Should Succeed')
    print(list(tokenD.keys()))
    print(list(functionD.keys()))
    print(errorStr)
    print('='*44)
    print('Should FAIL with ending extra paren')
    tokenD, functionD, errorStr = get_const_list( rhs_eqnStr= "A*sin(B*x)*x**2)")
    print(list(tokenD.keys()))
    print(list(functionD.keys()))
    print(errorStr)
    
