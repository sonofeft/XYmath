import unittest
# import unittest2 as unittest # for versions of python < 2.7
from numpy import array, double

import sys
sys.path.append("../")
from xymath.dataset import DataSet
from xymath.nonlinfit import NonLinCurveFit

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
        nlf = NonLinCurveFit( self.myds, rhs_eqnStr='A*sin(2*pi*k*x+theta)', 
                fit_best_pcent=1, constDinp=None)
        
    def test_myclass_existence(self):
        """Check that myclass exists"""
        result = self.myds
        # See if the self.myds object exists
        self.assertTrue(result)

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

