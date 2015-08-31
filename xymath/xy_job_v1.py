#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
A GUI and API that creates, documents and explores y=f(x) curve fits

<Paragraph description see docstrings at http://www.python.org/dev/peps/pep-0257/>
XYmath will find the "best" curve fit using either
      minimum percent error or minimum total error. It can search through
      common equations, an exhaustive search through thousands of equations,
      splines, smoothed splines, or non-linear equations input by the user.
      After fitting, XYmath will find roots, minima, maxima, derivatives or
      integrals of the curve. It will generate source code that documents and
      evaluates the fit in python, FORTRAN or EXCEL. Configurable plots are
      created using matplotlib that are of publication quality.

XYmath
Copyright (C) 2015  Charlie Taylor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
from builtins import object
import os
here = os.path.abspath(os.path.dirname(__file__))


__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2013 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "charlietaylor@users.sourceforge.net"
__status__ = "4 - Beta" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"

#
# import statements here. (built-in first, then 3rd party, then yours)
#
# Code goes below.
# Adjust docstrings to suite your taste/requirements.
#

class XY_Job(object):
    """A GUI and API that creates, documents and explores y=f(x) curve fits

    Longer class information....
    Longer class information....

    Attributes::
    
        likes_spam: A boolean indicating if we like SPAM or not.

        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self):
        """Inits XY_Job with blah."""
        self.likes_spam = True
        self.eggs = 3

    def public_method(self, arg1, arg2, mykey=True):
        """Performs operation blah.
        
        :param arg1: description of arg1
        :param arg2: description of arg2
        :type arg1: int
        :type arg2: float
        :keyword mykey: a needed input
        :type mykey: boolean
        :return: None
        :rtype: None
        
        .. seealso:: blabla see stuff
        
        .. note:: blabla noteworthy stuff
        
        .. warning:: blabla arg2 must be non-zero.
        
        .. todo:: blabla  lots to do
        """
        #  Answer to the Ultimate Question of Life, The Universe, and Everything
        return 42

if __name__ == '__main__':
    C = XY_Job()
