

.. image:: https://travis-ci.org/sonofeft/XYmath.svg?branch=master
    :target: https://travis-ci.org/sonofeft/XYmath

.. image:: https://img.shields.io/pypi/v/XYmath.svg
    :target: https://pypi.python.org/pypi/xymath
        
.. image:: https://img.shields.io/pypi/pyversions/XYmath.svg
    :target: https://wiki.python.org/moin/Python2orPython3

.. image:: https://img.shields.io/pypi/l/XYmath.svg
    :target: https://pypi.python.org/pypi/xymath


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

