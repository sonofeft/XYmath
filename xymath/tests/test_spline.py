import unittest
# import unittest2 as unittest # for versions of python < 2.7

from numpy import empty, ones, array, double, dot, vstack, std, sqrt

import sys
sys.path.append("../")
from xymath.dataset import DataSet
from xymath.linfit import LinCurveFit
from xymath.splines import Spline

xArr = array( [1,2,3,4,5,6], dtype=double)
yArr = array( [1,4,9,16,25,36], dtype=double)

class MyTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.myds = DataSet(xArr, yArr)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del( self.myds )

    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass
        
    def test_myclass_existence(self):
        """Check that myclass exists"""
        result = self.myds
        
        # See if the self.myds object exists
        self.assertTrue(result)
        
    def test_get_linear_spline(self):
        """get LinCurveFit for constant"""
        s = Spline( self.myds, order=1, smoothing=0.0)
        val = s.eval_xrange( 2.5 )
        refVal = 6.5
        self.assertAlmostEqual(val, refVal)
        
    def test_get_quadratic_spline(self):
        """get Quadratic Spline for constant"""
        s = Spline( self.myds, order=2, smoothing=0.0)
        val = s.eval_xrange( 2.5 )
        refVal = 6.25
        self.assertAlmostEqual(val, refVal)
        
    def test_get_smooth_linear_spline(self):
        """get LinCurveFit for constant"""
        s = Spline( self.myds, order=1, smoothing=1.0)
        val = s.eval_xrange( 2.5 )
        refVal = 6.869098813825232 #6.5
        self.assertAlmostEqual(val, refVal)
        

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

