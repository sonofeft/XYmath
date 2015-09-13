"""
Example from: http://www.walkingrandomly.com/?p=5215

The author (Mike Croucher) wants to fit the equation: p1*cos(p2*x) + p2*sin(p1*x)
He makes an initial guess of p1=1 and p2=0.2 and gets an answer of:
p1 = 1.88184732
p2 = 0.70022901

With no initial guess, XYmath gets:
p1 = 1.88185084847
p2 = 0.70022981688

1) Launch XYmath with code below
2) Go to "Non-Linear Fit" Tab 
   - should see "p1*cos(p2*x) + p2*sin(p1*x)" in eqn box
3) Hit "Curve Fit"
4) See what happens when you hit "Improve Fit" a few times
5) Change to "Percent Error" and notice changes

"""

from xymath.xy_job import XY_Job
from xymath.gui.xygui import main as run_gui

XY = XY_Job()

xdata = [-2,-1.64,-1.33,-0.7,0,0.45,1.2,1.64,2.32,2.9]
ydata = [0.699369,0.700462,0.695354,1.03905,1.97389,2.41143,1.91091,0.919576,-0.730975,-1.42001]

XY.define_dataset(xdata, ydata, wtArr=None, xName='x', yName='y', xUnits='', yUnits='')

XY.fit_dataset_to_nonlinear_eqn(run_best_pcent=0, rhs_eqnStr='p1*cos(p2*x) + p2*sin(p1*x)')

run_gui( XY )

