"""
the website
http://www.engineeringtoolbox.com/air-altitude-pressure-d_462.html

Calculates air pressure above sea level as:
pressure(Pa)  = 101325 (1 - 2.25577 10-5 h)^5.25588   
where x=altitude(m)

1) Launch XYmath with code below
2) Go to "Non-Linear Fit" Tab
   - Should see "A*(c - d*x)**n" in eqn box
3) Hit "Curve Fit"
4) Note that XYmath's initial guess of 1.0 for all params is not good
5) Correct resulting "nan" (Not a Number) to websites values (see below)
6) Hit "Set Constants" Button
7) Use "Math" tab enter "X=" 10000, hit "Evaluate Y & dY/dX at X" Button
   Verify that XYmath evaluates to the same as website

        y = A*(c - d*x)**n
            A = 101325.0
            c = 1.0
            d = 2.25577e-05
            n = 5.25588
            x = altitude (m)
            y = Pressure (Pa)
            Correlation Coefficient = 0.999995821319
            Standard Deviation = 93.2374437135
            Percent Standard Deviation = 0.106440180482%
        y = 101325.0*(1.0 - 2.25577e-05*x)**5.25588

        Website calculates pressure at 10,000 m as:
        p = 101325 (1 - 2.25577 10-5 (10000 m))^5.25588 
          = 26436 Pa
        XYmath value =   26436.2 Pa

8) Go back to "Non-Linear Fit" tab and hit "Improve Fit" Button
   XYmath improves fit slightly in terms of StdDev and Percent StdDev

        y = A*(c - d*x)**n
            A = 101071.995075
            c = 1.00050869652
            d = 2.22270597814e-05
            n = 5.34803672307
            x = altitude (m)
            y = Pressure (Pa)
            Correlation Coefficient = 0.999996164903
            Standard Deviation = 88.4289426009
            Percent Standard Deviation = 0.0992975318388%
"""
from numpy import array, double
from xymath.xy_job import XY_Job
from xymath.gui.xygui import main as run_gui

XY = XY_Job()

alt_mArr = array([-1524,-1372,-1219,-1067,-914,-762,-610,-457,-305,-152,0,152,
           305,457,610,762,914,1067,1219,1372,1524,1829,2134,2438,2743,3048,4572,
           6096,7620,9144,10668,12192,13716,15240], dtype=double)

PaArr = 1000.0 * array([121,119,117,115,113,111,109,107,105,103,101,99.5,97.7,96,
        94.2,92.5,90.8,89.1,87.5,85.9,84.3,81.2,78.2,75.3,72.4,69.7,57.2,46.6,37.6,
        30.1,23.8,18.7,14.5,11.1], dtype=double)

XY.define_dataset(alt_mArr, PaArr, wtArr=None, xName='altitude', yName='Pressure', 
                  xUnits='m', yUnits='Pa')


guessD = {'A':100000, 'c':1, 'd':0.00001, 'n':4  }
    
XY.fit_dataset_to_nonlinear_eqn(run_best_pcent=0, rhs_eqnStr='A*(c - d*x)**n', 
                                constDinp=guessD)

run_gui( XY )
