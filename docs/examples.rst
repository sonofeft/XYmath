
.. examples


.. _internal_examples:

Example Scripts
===============

There are several ways to run XYmath
    
    1. Launch the GUI, enter and fit data and perhaps run some math operations 
        - (see :ref:`internal_launch_gui` and :ref:`internal_entering_data` and :ref:`internal_math_ops`)
    2. Write a script to launch the GUI with data
    3. Run a script that outputs to the console
    
The examples that follow will show both GUI and console scripts (options 2 & 3).

.. warning::
    It is dangerous to run a console curve fit and accept it without looking at a plot.
    
    Curve fitting is mostly about what happens **Between** the points, not **At** the points.

Instrument Calibration
----------------------

This example comes from: http://terpconnect.umd.edu/~toh/spectrum/CurveFitting.html

The author shows a linear fit of an instrument reading chemical concentrations

The author mentions that a quadratic fit w/o the data point at 
concentration=0.6 would be significantly better... that is also calculated.

With GUI
~~~~~~~~

The script ``/xymath/examples/calibration_gui.py`` launches the XYmath GUI with the calibration data so that the GUI can perform the desired calculations.

.. code:: python

    from numpy import array
    from xymath.dataset import DataSet
    from xymath.linfit import LinCurveFit
    from xymath.xy_job import XY_Job
    from xymath.gui.xygui import main as run_gui

    concL = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    readingL = [1.54,2.03,3.17,3.67,4.89,6.73,6.74,7.87,8.86,10.35]
    DS = DataSet(concL, readingL, xName='Concentration', yName='Instrument Reading')

    XY = XY_Job()
    XY.define_dataset(concL, readingL, wtArr=None, xName='Concentration', 
                      yName='Instrument Reading', xUnits='', yUnits='')
    run_gui( XY )

Once launched, the following steps can be taken inside the GUI::

        1) Launch XYmath with code above
        2) Go to "Simple Fit" Tab 
        3) Hit "Curve Fit"
            - XYmath will show "c0 + c1/x + c2/x**2 + c3*x" as best fit
        4) Select "y = c0 + c1*x" to approximate the author's results
        5) Go to "Data" Tab
        6) Select "weight" of data point with concentration=0.6
            - Set that weight to 0.0
        7) Go back to "Simple Fit" Tab and hit "Curve Fit"
            - Notice that the zero-weighted point is marked as such on the plot
            - As the author predicts, the fit is greatly improved
            - Surprisingly, XYmath shows the 3 term equation "y = c0 + c1*x + c2/x"
              to be superior to the 4 term equations as well as the quadratic.


Running the above code, launches the GUI, preloaded with the concentration data. 

**Using "Simple Fit" results in the GUI and plot shown below.**

.. image:: ./_static/ex_conc_simple_fit_gui.png
    :width: 52%
.. image:: ./_static/ex_conc_simple_fit_plot.png
    :width: 40%
   

**Selecting the straight line "y = c0 + c1*x" gives the GUI and plot shown below.**

.. image:: ./_static/ex_conc_simple_fit_gui_v2.png
    :width: 52%
.. image:: ./_static/ex_conc_simple_fit_plot_v2.png
    :width: 40%

**Use "Data" tab to set weight of data point at concentration=.6 to zero.**

.. image:: ./_static/ex_conc_simple_fit_gui_zerowt.png
    :width: 52%


**Rerun "Simple Fit" and select author's quadratic recommendation**

Notice that the data point at concentration=0.6 is still on the plot, but it is labeled as "Weighted Low" and it's weight value is indicated as "x0".

.. image:: ./_static/ex_conc_simple_fit_gui_zerowt_quad.png
    :width: 52%
.. image:: ./_static/ex_conc_simple_fit_gui_zerowt_quad_plot.png
    :width: 40%



With Console
~~~~~~~~~~~~

As you might imagine, the console script is longer because it performs many of the steps done manually in the GUI example.  

This example first duplicates the author's equation (i.e. sets the straight line coefficients to the same values as the author (``cArrInp=[0.199, 9.7926]``) and calculates standard deviation and percent standard deviation as a reference.

Then runs XYmath to fit the points. It results in only a very slight improvment in the author's answer (see output below python script).

And finally removes the point at concentration=0.6 and fits to a quadratic. This results in the big improvement that the author was looking for (see output below python script).

Here's the code from ``/xymath/examples/calibration.py``.


.. code:: python

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

**The console output is shown below**::

    =======================================================
    .... First show author's answer ....
    y = c0 + c1*x
        c0 = 0.199
        c1 = 9.7926
        x = Concentration
        y = Instrument Reading
        Correlation Coefficient = 0.993152645552
        Standard Deviation = 0.331007277412
        Percent Standard Deviation = 9.42865864393%
    y = 0.199 + 9.7926*x
    =======================================================
    .... Then show XYmath answer ....
    y = c0 + c1*x
        c0 = 0.196666666667
        c1 = 9.79696969697
        x = Concentration
        y = Instrument Reading
        Correlation Coefficient = 0.993152645552
        Standard Deviation = 0.331004897886
        Percent Standard Deviation = 9.45154746872%
    y = 0.196666666667 + 9.79696969697*x
    =======================================================
    .... Then show XYmath Quadratic answer ....
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

**If matplotlib is installed on your machine, then you should see the following plot**

.. image:: ./_static/ex_conc_console_fit_plot.png

