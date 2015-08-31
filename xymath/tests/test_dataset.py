import unittest
# import unittest2 as unittest # for versions of python < 2.7

from numpy import empty, ones, array, double, dot, vstack, std, sqrt

import sys
sys.path.append("../")
from xymath.dataset import DataSet

xArr = array( [1,2,3,4,5,6], dtype=double)
yArr = array( [10,5.49,0.89,-.14,-1.07,0.84], dtype=double)

#  y = 3.3888 + 0.3725*x
xArr2 = array( [1, 3, 5, 7, 10, 12, 13, 16, 18, 20], dtype=double)
yArr2 = array( [4, 5, 6, 5,  8,  7,  6,  9, 12, 11], dtype=double)

class MyTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        xArrNew = array( [1,2,3,4,5,6], dtype=double)
        yArrNew = array( [10,5.49,0.89,-.14,-1.07,0.84], dtype=double)
        self.myclass = DataSet(xArrNew, yArrNew,
            xName='xxx', yName='yyy', xUnits='sec', yUnits='ft', timeStamp=123.45)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del( self.myclass )

    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass
        
    def test_myclass_existence(self):
        """Check that myclass exists"""
        result = self.myclass
        # See if the self.myclass object exists
        self.assertTrue(result)
        
    def test_get_x_transform_for_constant(self):
        """get x transform for constant"""
        val = self.myclass.getTransXArr(name='const')
        self.assertTrue((val==ones(6, dtype=double)).all())

    def test_get_x_transform_for_x(self):
        """get x transform for x"""
        val = self.myclass.getTransXArr(name='x')
        self.assertTrue((val==xArr).all())

    def test_get_x_transform_for_1_over_x(self):
        """get x transform for x"""
        val = self.myclass.getTransXArr(name='1/x')
        self.assertTrue((val==1.0/xArr).all())

    def test_get_x_transform_for_x2(self):
        """get x transform for x"""
        val = self.myclass.getTransXArr(name='x**2')
        self.assertTrue((val==xArr**2).all())

    def test_get_x_transform_for_y(self):
        """get y transform for y"""
        val = self.myclass.getTransYArr(name='y')
        self.assertTrue((val==yArr).all())

    def test_data_append(self):
        """append a row of data"""
        self.myclass.append_xy( 7.0, 0.7 )
        xnewArr = array( [1,2,3,4,5,6,7], dtype=double)
        self.assertTrue((self.myclass.xArr==xnewArr).all())
        
        ynewArr = array( [10,5.49,0.89,-.14,-1.07,0.84, 0.7], dtype=double)
        self.assertTrue((self.myclass.yArr==ynewArr).all())

    def test_data_append_list(self):
        """append new rows of data"""
        self.myclass.append_xy_list( [7.0,8.0], [0.7,0.8] )
        xnewArr = array( [1,2,3,4,5,6,7,8], dtype=double)
        self.assertTrue((self.myclass.xArr==xnewArr).all())
        
        ynewArr = array( [10,5.49,0.89,-.14,-1.07,0.84, 0.7,0.8], dtype=double)
        self.assertTrue((self.myclass.yArr==ynewArr).all())

    def test_data_append_with_wts(self):
        """append a row of data"""
        self.myclass.set_all_weights_to_one()
        self.myclass.append_xy( 7.0, 0.7 )
        wnewArr = ones( 7, dtype=double)
        self.assertTrue((self.myclass.wtArr==wnewArr).all())

    def test_data_append_list_with_wts(self):
        """append new rows of data"""
        self.myclass.set_all_weights_to_one()
        self.myclass.append_xy_list( [7.0,8.0], [0.7,0.8] )
        wnewArr = ones( 8, dtype=double)
        self.assertTrue((self.myclass.wtArr==wnewArr).all())

    def test_data_set_xy(self):
        """set an xy pair"""
        self.myclass.set_an_xy_pair( 2, 3.33, 3.89)
        xnewArr = array( [1,2,3.33,4,5,6], dtype=double)
        self.assertTrue((self.myclass.xArr==xnewArr).all())
        
        ynewArr = array( [10,5.49,3.89,-.14,-1.07,0.84], dtype=double)
        self.assertTrue((self.myclass.yArr==ynewArr).all())

    def test_replace_all_xy_data(self):
        """set all xy data"""
        self.myclass.replace_all_xy_data(xArr=array([1.,2.]), yArr=array([3.,4.]))
        xnewArr = array( [1,2], dtype=double)
        self.assertTrue((self.myclass.xArr==xnewArr).all())
        
        ynewArr = array( [3,4], dtype=double)
        self.assertTrue((self.myclass.yArr==ynewArr).all())

    def test_swap_x_and_y_data(self):
        """swap xArr and yArr data"""
        self.myclass.summary_print()
        print( '#'*66 )
        self.myclass.swap_x_and_y()
        self.myclass.summary_print()
        ynewArr = array( [1,2,3,4,5,6], dtype=double)
        xnewArr = array( [10,5.49,0.89,-.14,-1.07,0.84], dtype=double)
        
        self.assertTrue((self.myclass.xArr==xnewArr).all())
        self.assertTrue((self.myclass.yArr==ynewArr).all())


    def test_sort_data(self):
        """sort xArr and yArr data by xArr"""
        self.myclass.replace_all_xy_data( xArr=array([2,7,1,4]), yArr=array([22.2,0.7,11.1,4.4]), wtArr=None)
        self.myclass.summary_print()
        print( '#'*66 )
        self.myclass.sort_by_x()
        self.myclass.summary_print()
        xnewArr = array( [1,2,4,7], dtype=double)
        ynewArr = array( [11.1,22.2,4.4,0.7], dtype=double)
        
        self.assertTrue((self.myclass.xArr==xnewArr).all())
        self.assertTrue((self.myclass.yArr==ynewArr).all())
        

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

