"""
Example from: http://terpconnect.umd.edu/~toh/spectrum/CurveFitting.html

The author shows a linear fit of an instrument reading concentrations.
        
The author mentions that a quadratic fit w/o the data point at 
concentration=0.6 would be significantly better... that is also calc'd

1) Launch XYmath with code below
2) Go to "Simple Fit" Tab 
3) Hit "Curve Fit"
    - XYmath will show "c0 + c1/x + c2/x**2 + c3*x" as best fit
4) Select "y = c0 + c1*x" to duplicate the author's results
5) Go to "Data" Tab
6) Select "weight" of data point with concentration=0.6
    - Set that weight to 0.0
7) Go back to "Simple Fit" Tab and hit "Curve Fit"
    - Notice that the zero-weighted point is marked as such on the plot
    - As the author predicts, the fit is greatly improved
    - Surprisingly, XYmath shows the 3 term equation "y = c0 + c1*x + c2/x"
      to be superior to the 4 term equations as well as the quadratic.


"""
from numpy import array
from xymath.dataset import DataSet
from xymath.linfit import LinCurveFit
from xymath.xy_job import XY_Job
from xymath.gui.xygui import main as run_gui

concL = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
readingL = [1.54,2.03,3.17,3.67,4.89,6.73,6.74,7.87,8.86,10.35]
DS = DataSet(concL, readingL, xName='Concentration', yName='Instrument Reading')

print('\n\n')
print('='*55)

XY = XY_Job()
XY.define_dataset(concL, readingL, wtArr=None, xName='Concentration', 
                  yName='Instrument Reading', xUnits='', yUnits='')
run_gui( XY )

