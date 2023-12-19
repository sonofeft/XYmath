

.. image:: https://img.shields.io/pypi/v/XYmath.svg
        
.. image:: https://img.shields.io/badge/python-3.5|3.6|3.7|3.8|3.9|3.10-blue

.. image:: https://img.shields.io/pypi/l/XYmath.svg


XYmath Creates, Documents And Explores Y=f(X) Curve Fits
========================================================

See the Code at: `<https://github.com/sonofeft/XYmath>`_

See the Docs at: `<http://xymath.readthedocs.org/en/latest/>`_

See PyPI page at:`<https://pypi.python.org/pypi/xymath>`_

XYmath will find the "best" curve fit equation in a data set of x,y pairs by minimizing
the sum of the square of the the difference between the data and the equation (i.e. residuals).  

The user may choose to minimize either percent error or total error.  

*(Percent error is particularly useful for y values spanning several orders of magnitude.)*

XYmath can search through
common equations, an exhaustive search through thousands of equations,
splines, smoothed splines, or fit non-linear equations of the user's choice.

After fitting, XYmath will find roots, minima, maxima, derivatives or
integrals of the fitted curve. It will generate source code that documents and
evaluates the fit in python, FORTRAN or EXCEL. Configurable plots are
created using matplotlib that are of publication quality, including plots of
equation residuals.

