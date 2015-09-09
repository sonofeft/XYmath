from numpy import array, double

from xymath import xy_job
from xymath.gui.xygui import main as run_gui

XY = xy_job.XY_Job()

"""
http://www.engineeringtoolbox.com/air-altitude-pressure-d_462.html

Air pressure above sea level can be calculated as

p = 101325 (1 - 2.25577 10-5 h)^5.25588             (1)

where

p = air pressure (Pa)

h = altitude above sea level (m)

Example - Air pressure at Elevation 10000 m
The air pressure at altitude 10000 m can be calculated as

p = 101325 (1 - 2.25577 10-5 (10000 m))^5.25588 

  = 26436 Pa
"""

alt_ftL = [-5000,-4500,-4000,-3500,-3000,-2500,-2000,-1500,-1000,-500,0,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,6000,7000,8000,9000,10000,15000,20000,25000,30000,35000,40000,45000,50000]
alt_mL = [-1524,-1372,-1219,-1067,-914,-762,-610,-457,-305,-152,0,152,305,457,610,762,914,1067,1219,1372,1524,1829,2134,2438,2743,3048,4572,6096,7620,9144,10668,12192,13716,15240]

mmHgL = [908,892,876,861,846,831,816,802,788,774,760,746,733,720,707,694,681,669,656,644,632,609,586,564,543,523,429,349,282,226,179,140,109,83]
kPaL = [121,119,117,115,113,111,109,107,105,103,101,99.5,97.7,96,94.2,92.5,90.8,89.1,87.5,85.9,84.3,81.2,78.2,75.3,72.4,69.7,57.2,46.6,37.6,30.1,23.8,18.7,14.5,11.1]

alt_mL = [x+3000 for x in alt_mL]
XY.define_dataset(alt_mL, kPaL, wtArr=None, xName='altitude', yName='Pressure', xUnits='m', yUnits='kPa')

run_gui( XY )

"""
Verifying ref fit:
Improving Fit's Total Error.

XYmath values
y = A*(c - d*x)**n
    A = 101.995825759
    c = 0.998807944724
    d = 2.21892761502e-05
    n = 5.34803675929
    x = altitude (m)
    y = Pressure (kPa)
    Correlation Coefficient = 0.999996164903
    Standard Deviation = 0.0884289396418
    Percent Standard Deviation = 0.0992975480686%
y = 101.995825759*(0.998807944724 - 2.21892761502e-05*x)**5.34803675929

website values
y = A*(c - d*x)**n
    A = 101.325
    c = 1.0
    d = 2.25577e-05
    n = 5.25588
    x = altitude (m)
    y = Pressure (kPa)
    Correlation Coefficient = 0.999995821319
    Standard Deviation = 0.0932374437135
    Percent Standard Deviation = 0.106440180482%
y = 101.325*(1.0 - 2.25577e-05*x)**5.25588

"""
