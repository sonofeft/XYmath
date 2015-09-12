"""
Example from: http://terpconnect.umd.edu/~toh/spectrum/CurveFitting.html

The author shows a linear fit of an instrument reading concentrations.
        .... author's answer ....
        y = c0 + c1*x
            c0 = 0.199
            c1 = 9.7926
            x = Concentration
            y = Instrument Reading
            Correlation Coefficient = 0.993152645552
            Standard Deviation = 0.331007277412
            Percent Standard Deviation = 9.42865864393%
        y = 0.199 + 9.7926*x
        
        The author mentions that a quadratic fit w/o the data point at 
        concentration=0.6 would be significantly better... that is also calc'd


1) run script and get virtually identical results
        .... XYmath answer ....
        y = c0 + c1*x
            c0 = 0.196666666667
            c1 = 9.79696969697
            x = Concentration
            y = Instrument Reading
            Correlation Coefficient = 0.993152645552
            Standard Deviation = 0.331004897886
            Percent Standard Deviation = 9.45154746872%
        y = 0.196666666667 + 9.79696969697*x


        .... XYmath Quadratic answer without data point at concentration=0.6 ....
        y = c0 + c1*x + c2*x**2
            c0 = 0.8315625
            c1 = 6.22254971591
            c2 = 3.19353693182
            x = Concentration
            y = Instrument Reading
            Correlation Coefficient = 0.999039190283
            Standard Deviation = 0.129698349765
            Percent Standard Deviation = 4.11221905227%
        y = 0.8315625 + 6.22254971591*x + 3.19353693182*x**2

"""
try:
    from matplotlib import pyplot as plt
    got_plt = True
except:
    got_plt = False
    
from xymath.dataset import DataSet
from xymath.linfit import LinCurveFit

concL = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
readingL = [1.54,2.03,3.17,3.67,4.89,6.73,6.74,7.87,8.86,10.35]
DS = DataSet(concL, readingL, xName='Concentration', yName='Instrument Reading')

print('\n\n')
print('='*55)
print(".... First show author's answer ....")
Fit_ref = LinCurveFit(DS, xtranL=['const', 'x'] , ytran='y', cArrInp=[0.199, 9.7926],
                  fit_best_pcent=0)   # 0=fit best total error
print(Fit_ref.get_full_description())

print('='*55)
print('.... Then show XYmath answer ....')
Fit_linear = LinCurveFit(DS, xtranL=['const', 'x'] , ytran='y', 
                  fit_best_pcent=0)   # 0=fit best total error
print(Fit_linear.get_full_description())

print('='*55)
print('.... Then show XYmath Quadratic answer ....')

v2_concL =    [0.1,  0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1]
v2_readingL = [1.54,2.03,3.17,3.67,4.89,6.74,7.87,8.86,10.35]
DS = DataSet(v2_concL, v2_readingL, xName='Concentration', yName='Instrument Reading')

Fit_quad = LinCurveFit(DS, xtranL=['const', 'x', 'x**2'] , ytran='y', 
                  fit_best_pcent=0)   # 0=fit best total error
print(Fit_quad.get_full_description())

if got_plt:
    plt.plot( concL, readingL, 'o', markersize=10  )
    xPlotArr, yPlotArr = Fit_ref.get_xy_plot_arrays( Npoints=100, logScale=False)
    plt.plot( xPlotArr, yPlotArr, '--', linewidth=4  )
    xPlotArr, yPlotArr = Fit_linear.get_xy_plot_arrays( Npoints=100, logScale=False)
    plt.plot( xPlotArr, yPlotArr, '-'  )
    xPlotArr, yPlotArr = Fit_quad.get_xy_plot_arrays( Npoints=100, logScale=False)
    plt.plot( xPlotArr, yPlotArr, '-'  )
    plt.title('Calibration Example')
    plt.show()
