"""
the website
http://www.engineeringtoolbox.com/air-altitude-pressure-d_462.html

Calculates air pressure above sea level as:
pressure(Pa)  = 101325 (1 - 2.25577 10-5 h)^5.25588   
where x=altitude(m)

1) run script and get slightly improved answer from web site
   (Note that Percent Error fit has better %StdDev but worse StdDev)

        ..........Total Error............
        y = A*(c - d*x)**n
            A = 101071.995075
            c = 1.00050869652
            d = 2.22270597814e-05
            n = 5.34803672307
            x = altitude (m)
            y = pressure (Pa)
            Correlation Coefficient = 0.999996164903
            Standard Deviation = 88.4289426009
            Percent Standard Deviation = 0.0992975318388%
        y = 101071.995075*(1.00050869652 - 2.22270597814e-05*x)**5.34803672307
        =======================================================
        ..........Percent Error............
        y = A*(c - d*x)**n
            A = 101749.173838
            c = 0.999255692815
            d = 2.2309845172e-05
            n = 5.31856519674
            x = altitude (m)
            y = pressure (Pa)
            Correlation Coefficient = 0.999996135864
            Standard Deviation = 88.7614426959
            Percent Standard Deviation = 0.0944017487367%
        y = 101749.173838*(0.999255692815 - 2.2309845172e-05*x)**5.31856519674

2) Set constants to website values and see slightly higher StdDev and Percent StdDev
   than the XYmath fit.
   
        y = A*(c - d*x)**n
            A = 101325
            c = 1
            d = 2.25577e-05
            n = 5.25588
            x = altitude (m)
            y = pressure (Pa)
            Correlation Coefficient = 0.999995821319
            Standard Deviation = 93.2374437135
            Percent Standard Deviation = 0.106440180482%
        y = 101325*(1 - 2.25577e-05*x)**5.25588

"""
from numpy import array, double
from xymath.dataset import DataSet
from xymath.nonlinfit import NonLinCurveFit

alt_mArr = array([-1524,-1372,-1219,-1067,-914,-762,-610,-457,-305,-152,0,152,305,457,
          610,762,914,1067,1219,1372,1524,1829,2134,2438,2743,3048,4572,6096,7620,
          9144,10668,12192,13716,15240], dtype=double)

PaArr = 1000.0 * array([121,119,117,115,113,111,109,107,105,103,101,99.5,97.7,96,94.2,92.5,90.8,
        89.1,87.5,85.9,84.3,81.2,78.2,75.3,72.4,69.7,57.2,46.6,37.6,30.1,23.8,
        18.7,14.5,11.1], dtype=double)
        
DS = DataSet(alt_mArr, PaArr, xName='altitude', yName='pressure', xUnits='m', yUnits='Pa')


guessD = {'A':101325, 'c':1, 'd':2.25577E-5, 'n':5.25588  }
print( 'guessD Before',guessD )
CFit = NonLinCurveFit(DS, rhs_eqnStr='A*(c - d*x)**n', 
                                constDinp=guessD, fit_best_pcent=0)   # 0=fit best total error
print( 'guessD After',guessD )

print('='*55)
print('..........Total Error............')
print(CFit.get_full_description())
print('='*55)
print('..........Percent Error............')
CFit = NonLinCurveFit(DS, rhs_eqnStr='A*(c - d*x)**n', 
                                constDinp=guessD, fit_best_pcent=1)   # 0=fit best total error
print(CFit.get_full_description())
print('='*55)

# To set parameters to something other than "Best Fit" values do this:
CFit.constD.update( {'A':101325, 'c':1, 'd':2.25577E-5, 'n':5.25588  } )
CFit.calc_std_values()
print(CFit.get_full_description())

