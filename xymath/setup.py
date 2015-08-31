#!/usr/bin/env python
# setup.py 
from distutils.core import setup 

setup(name="XYmath",
      version='0.1.6',
      description = 'A GUI and API that creates, documents and explores y=f(x) curve fits',
      author="Charlie Taylor",
      author_email="charlietaylor@users.sourceforge.net",
      url='https://sourceforge.net/projects/xymath/',
      package_dir = { "xymath":""},
      packages=['xymath','xymath.gui'],
      package_data={'': ['LICENSE.TXT','COPYING.TXT']},
      license='GPLv3',
      long_description='''XYmath will find the "best" curve fit using either
      minimum percent error or minimum total error. It can search through
      common equations, an exhaustive search through thousands of equations,
      splines, smoothed splines, or non-linear equations input by the user.
      After fitting, XYmath will find roots, minima, maxima, derivatives or
      integrals of the curve. It will generate source code that documents and
      evaluates the fit in python, FORTRAN or EXCEL. Configurable plots are
      created using matplotlib that are of publication quality..''',
      classifiers = [
          'Development Status :: Beta',
          'Environment :: Win32 (MS Windows)',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'License :: GPLv3+',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering',
          'Topic :: Education',
          ],
    data_files=[('', [ 'XYmath128.ico', 'xymath.bat'])],
     )
