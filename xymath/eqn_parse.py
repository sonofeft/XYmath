#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
Parse the right hand side of a user-defined equation y=f(x)
"""
from __future__ import print_function


import parser
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
    
    def search(st):
        if not isinstance(st, list):
            return
        if st[0] in [token.NAME]:
            #print st[1]
            if st[1] in legalFuncL:
                functionD[st[1]] = st[1]
            else:
                tokenD[st[1]] = st[1]
        else:
            for s in st[1:]:
                search(s)
    
    try:
        ast = parser.expr( rhs_eqnStr )
        eqnL = parser.ast2list( ast )
        search( eqnL )
        #print tokenD    
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
    print(list(tokenD.keys()))
    print(list(functionD.keys()))
    print(errorStr)
    print('='*44)
    tokenD, functionD, errorStr = get_const_list( rhs_eqnStr= "A*sin(B*x)*x**2)")
    print(list(tokenD.keys()))
    print(list(functionD.keys()))
    print(errorStr)
    
