#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
Support routines for exhaustive equation search in curve fit routines.

Uses itertools to find all combinations.
"""
from __future__ import print_function
from builtins import str


from itertools import combinations
from math import factorial

full_funcL = ['const','x','x**2','x**3','x**4','x**5','x**6','log(x)','exp(x)']

full_xtranL = ['x','1/x','log(x)','exp(x)','(1/log(x))','log(1/x)','(1/exp(x))','exp(1/x)']

full_ytranL = ['y','1/y','y**2','y**3','log(y)','exp(y)','1/log(y)','log(1/y)','1/exp(y)','exp(1/y)']


def next_term( func='x', xtranL=None ):
    k = func.rfind('x')
    if k==-1:
        yield func
    else:
        for xt in xtranL:
            # try to avoid double parens
            if '(x)'in func and xt[0]=='('  and xt[-1]==')':
                yield func[:k-1] + xt + func[k+2:]
            else:
                yield func[:k] + xt + func[k+1:]

def build_xterms( funcL=None, xtranL=None ):
    termL = []
    for f in funcL:
        for nt in next_term(func=f, xtranL=xtranL):
            if nt not in termL:
                termL.append( nt )
    return termL

# copied from itertools doc page. 
# http://docs.python.org/2/library/itertools.html#itertools.combinations
def num_combinations(iterable, r):
    n = len(iterable)
    if r>n:
        return 0
    return factorial(n) / factorial(r) / factorial(n-r)

if __name__ == "__main__":        
    
    for nt in next_term(func='x', xtranL=full_xtranL):
        print(nt)
    print()
    funcL=['const','x','x**2','exp(x)']
    xtranL=['x','(1/x)','exp(x)']
    print("termL for funcL=%s\n and xtranL=%s\n"%(str(funcL), str(xtranL)))
    
    termL = build_xterms( funcL=funcL, xtranL=xtranL )
    print(termL)
    print()
    print('# 3 Term equations =',num_combinations(termL, 3))
    for i,rhs in enumerate(combinations(termL, 3)):
        print('%3i)'%(i+1,),rhs)
    