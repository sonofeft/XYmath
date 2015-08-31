import unittest
# import unittest2 as unittest # for versions of python < 2.7

from numpy import empty, ones, array, double, dot, vstack, std, sqrt

import sys
sys.path.append("../")
from xymath.dataset import DataSet
from xymath.linfit import LinCurveFit

xArr = array( [1,2,3,4,5,6], dtype=double)
yArr = array( [10,5.49,0.89,-.14,-1.07,0.84], dtype=double)

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
        
    def test_get_fit_for_constant(self):
        """get LinCurveFit for constant"""
        lf = LinCurveFit( self.myds, ['const'], fit_best_pcent=0)
        val = lf.cArr[0]
        refVal = 2.6683333333333348
        self.assertAlmostEqual(val, refVal)

    def test_get_linear_fit(self):
        """get linear fit"""
        lf = LinCurveFit( self.myds, ['const', 'x'], fit_best_pcent=0)
        val = lf.cArr[0]
        refVal = 9.3193333333333399
        self.assertAlmostEqual(val, refVal)
        val = lf.cArr[1]
        refVal = -1.9002857142857148
        self.assertAlmostEqual(val, refVal)

    def test_get_quadratic_fit(self):
        """get quadratic fit"""
        lf = LinCurveFit( self.myds, ['const', 'x', 'x**2'], fit_best_pcent=0)
        val = lf.cArr[0]
        refVal = 17.116
        self.assertAlmostEqual(val, refVal)
        val = lf.cArr[1]
        refVal = -7.7477857
        self.assertAlmostEqual(val, refVal)
        val = lf.cArr[2]
        refVal = 0.8353571428
        self.assertAlmostEqual(val, refVal)
        
        yArr = lf.eval_xrange( array([1.0, 2.0]) )
        refVal = 4.9618571428571432
        self.assertAlmostEqual(yArr[1], refVal)

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

