from __future__ import print_function
from __future__ import absolute_import
from builtins import zip
from .helper_funcs import is_number

'''Interpret input string as either 2 rows or 2 columns of numbers.'''

def get_xy_lists( sInp ):
    
    # start out making list of non-blank rows
    sL = sInp.split('\n')
    rowL = []
    for s in sL:
        s = s.strip()
        if s:
            rowL.append(s)
    
    xL = []
    yL = []
    xName = 'xData'
    yName = 'yData'
    numBadPairs = 0
    
    if len(rowL)==2:
        print('Interpret as 2 rows')
        val = rowL[0].replace(',',' ') # if comma delimited, change to space
        topL = val.split()
        val = rowL[1].replace(',',' ') # if comma delimited, change to space
        botL = val.split()
        for top,bot in zip(topL, botL):
            if is_number(top) and is_number(bot):
                xL.append( float(top) )
                yL.append( float(bot) )
            elif top and bot:
                if not is_number(top) and not is_number(bot):
                    xName = top
                    yName = bot
                else:
                    numBadPairs += 1
            else:
                numBadPairs += 1
    else:
        print('Interpret as 2 columns')
        for row in rowL:
            val = row.replace(',',' ') # if comma delimited, change to space
            vL = val.split()

            if len(vL)==2:
                c0 = vL[0].strip()
                c1 = vL[1].strip()
                if is_number(c0) and is_number(c1):
                    xL.append( float(c0) )
                    yL.append( float(c1) )
                elif not is_number(c0) and not is_number(c1):
                    xName = c0
                    yName = c1
                else:
                    numBadPairs += 1
            else:
                numBadPairs += 1

    if len(xL)==0:
        xName = ''
        yName = ''
    return xL, yL, xName, yName, numBadPairs


if __name__ == '__main__':
    
    print('Testing Column Pasting')
    sInp = '''
XName   YName
1.00	10.20
2.00	21.80
3.00	37.80
4.00	58.20
5.00	83.00
6.00	112.20
7.00	145.80
8.00	183.80
9.00	226.20
'''
    xL, yL, xName, yName, numBadPairs = get_xy_lists( sInp )
    print('                      numBadPairs =',numBadPairs)
    print('xName=%s, yName=%s'%(xName, yName))    
    print('xL=',xL)
    print('yL=',yL)
    # =========================================
    print('='*44)
    print('Testing Row Pasting')
    sInp = '''
    
Xname, 2	4	6	8	10	12	14
Yname, 14	42	86	146	222	314	422

'''
    xL, yL, xName, yName, numBadPairs = get_xy_lists( sInp )
    print('                      numBadPairs =',numBadPairs)
    print('xName=%s, yName=%s'%(xName, yName))
    print('xL=',xL)
    print('yL=',yL)

    # =========================================
    print('='*44)
    print('Testing Bad Data')
    sInp = '''
    
Xname, 2	4	6	8	10	12	14
Yname, 14	42	86a b c d e f g h i j kkk lmnop
'''
    xL, yL, xName, yName, numBadPairs = get_xy_lists( sInp )
    print('                      numBadPairs =',numBadPairs)
    print('xName=%s, yName=%s'%(xName, yName))
    print('xL=',xL)
    print('yL=',yL)
