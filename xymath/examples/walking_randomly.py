"""
Example from: http://www.walkingrandomly.com/?p=5215

The author (Mike Croucher) makes initial guess of p1=1 and p2=0.2 in eqn:
p1*cos(p2*x) + p2*sin(p1*x)
and then gets:
p1 = 1.88184732
p2 = 0.70022901
with sum of squared residuals = 0.053812696547933969


1) run script and get virtually identical results
   (Note that Mike Croucher and this script both fit to best total error, 
    not best percent error)

        XYmath gets:
        p1 = 1.881850994
        p2 = 0.700229857403
        with sum of squared residuals = 0.053812696418763392


"""
try:
    from matplotlib import pyplot as plt
    got_plt = True
except:
    got_plt = False
    
from numpy import array
from xymath.dataset import DataSet
from xymath.nonlinfit import NonLinCurveFit

xdata = array([-2,-1.64,-1.33,-0.7,0,0.45,1.2,1.64,2.32,2.9])
ydata = array([0.699369,0.700462,0.695354,1.03905,1.97389,2.41143,
               1.91091,0.919576,-0.730975,-1.42001])
DS = DataSet(xdata, ydata, xName='x', yName='y')

guessD = {'p1':1.0, 'p2':0.2}
CFit = NonLinCurveFit(DS, rhs_eqnStr='p1*cos(p2*x) + p2*sin(p1*x)', 
                      constDinp=guessD, fit_best_pcent=0)   # 0=fit best total error

print( 'residuals from XYmath = %g'%sum( (CFit.eval_xrange( xdata ) - ydata)**2 ) )
print( 'residuals from author = 0.053812696547933969' )
print('')
print(CFit.get_full_description())

if got_plt:
    plt.plot( xdata, ydata, 'o', markersize=10  )
    xPlotArr, yPlotArr = CFit.get_xy_plot_arrays( Npoints=100, logScale=False)
    plt.plot( xPlotArr, yPlotArr )
    plt.title('Trig Function: p1*cos(p2*x) + p2*sin(p1*x)')
    plt.show()


