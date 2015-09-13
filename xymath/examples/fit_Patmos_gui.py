"""
the website
http://www.engineeringtoolbox.com/air-altitude-pressure-d_462.html

Calculates air pressure above sea level as:
pressure(Pa)  = 101325 * (1 - 2.25577E-5 * h)**5.25588   
where x=altitude(m)

1) Launch XYmath with code below
2) Go to "Non-Linear Fit" Tab
   - Should see "A*(c - d*x)**n" in eqn box
3) Hit "Curve Fit"

    y = A*(c - d*x)**n
        A = 101351.958792
        c = 0.999991347618
        d = 2.22155669208e-05
        n = 5.34803660866
        x = altitude (m)
        y = Pressure (Pa)
        Correlation Coefficient = 0.999996164903
        Standard Deviation = 88.4289410055
        Percent Standard Deviation = 0.0992974873982%

4) Change the "Fit By" flag to "Percent Error".
   Notice the XYmath improves Percent StdDev fit very slightly

    y = A*(c - d*x)**n
        A = 101124.977819
        c = 1.00041249485
        d = 2.23356723474e-05
        n = 5.31856523127
        x = altitude (m)
        y = Pressure (Pa)
        Correlation Coefficient = 0.999996135864
        Standard Deviation = 88.761441745
        Percent Standard Deviation = 0.094401748723%
        
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
