import unittest
# import unittest2 as unittest # for versions of python < 2.7

import sys
from numpy import empty, ones, array, double, dot, vstack, std, sqrt

sys.path.append("../")
from xymath.dataset import DataSet
from xymath.linfit import LinCurveFit
from xymath.splines import Spline
from xymath.math_funcs import * # all functions

xArr = array( [1,2,3,4,5,6], dtype=double)
yArr = array( [1,4,9,9,4,1], dtype=double)

class MyTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.myds = DataSet(xArr, yArr)
        self.myspline = Spline( self.myds, order=2, smoothing=0.0)
        self.mylinterp = Spline( self.myds, order=1, smoothing=0.0)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass
        
    def test_min_max(self):
        """Check that function returns result"""
        x_min, y_min, x_max, y_max = find_min_max(self.myspline, xlo=1.0, xhi=6.0, xtol=1.0e-12)
        
        # Function should return None
        self.assertAlmostEqual(x_max, 3.5)
        
    def test_root(self):
        """Check that function returns result"""
        xRootArr, yRootArr = find_root(self.mylinterp, ygoal=6.5, xlo=1.0, xhi=6.0)
        
        # Function should return None
        self.assertAlmostEqual(yRootArr[0], 6.5)
        self.assertAlmostEqual(xRootArr[0], 2.5)

        
    def test_integral(self):
        """Check that function returns result"""
        integral, error = find_integral(self.mylinterp, xlo=1.0, xhi=6.0)
        
        # Function should return None
        self.assertAlmostEqual(integral, 27.0)
        self.assertAlmostEqual(error, 0.0, places=6)

        
    def test_derivs(self):
        """Check that function returns result"""
        resultL = find_values_at_x(self.mylinterp, 2.5, xlo=1.0, xhi=6.0)
        
        # Function should return None
        self.assertAlmostEqual(resultL[0], 6.5)
        self.assertAlmostEqual(resultL[1], 5)
        self.assertAlmostEqual(resultL[2], 0)


if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

