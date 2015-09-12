
.. quickstart

QuickStart
==========

.. _Python(x,y): http://python-xy.github.io/
.. _Anaconda: https://store.continuum.io/cshop/anaconda/


Prerequisites
-------------

XYmath dependencies include matplotlib, numpy, scipy, numexpr, imaging-tk (and win32com on Windows).
Installing these can be problematic on both Windows and Linux.
The easiest solution is to use Anaconda_ or `Python(x,y)`_.
If you are interested in XYmath, you probably want Anaconda_ or `Python(x,y)`_ for many other reasons anyway.

I recommend you go to either

Python(x,y): `<http://python-xy.github.io/>`_

Or

Anaconda: `<https://store.continuum.io/cshop/anaconda/>`_

and install the python 2.7 package of your choice

.. warning::

    Python 3.x has an error in matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
    that causes XYmath to crash and burn.
    
    XYmath python source is configured for python 3.x, but until
    the matplotlib folks fix FigureCanvasTkAgg, XYmath only runs on python 2.7

XYmath itself is a pure python package, all modules are written in python with no compiled extension modules of its own.


Without Anaconda or Python(x,y)
-------------------------------



w/o On Windows
~~~~~~~~~~~~~~

If you insist on "going it alone" without Anaconda_ or `Python(x,y)`_, on Windows, then I can't help you, I don't know how to install XYmath without one or the other of those environments.

I'm a Windows person with years of experience with python on Windows and I still find the process too daunting.

You really can't go wrong with either Anaconda_ or `Python(x,y)`_, I have used them both and think they are both excellent.  
`Python(x,y)`_ is only on Windows, Anaconda_ supports both Windows and Linux.


w/o On Linux
~~~~~~~~~~~~

Without Anaconda_ on Linux, note that pip will not install some packages.
You may get messages like: "the following required packages cannot be built * freetype png"
OR "i686-linux-gnu-gcc: error trying to exec 'cc1plus'".

You may need to do the following::

    Use the ``Software Manager`` to install matplotlib, numpy, scipy, numexpr, imaging-tk
    
    Or Try,
    
    sudo apt-get install python-matplotlib
    sudo apt-get install python-numpy
    sudo apt-get install python-scipy
    sudo apt-get install python-numexpr
    sudo apt-get install python-imaging-tk
    


Install XYmath
--------------

Once the above prerequisites are met,
the easiest way to install XYmath is::

    pip install xymath
    
        OR on Linux
    sudo pip install xymath
        OR perhaps
    pip install --user xymath

In case of error, see :ref:`internal_pip_error`
    

.. _internal_source_install:

Installation From Source
------------------------

Much less common, but if installing from source, then
the best way to install xymath is still ``pip``.

After navigating to the directory holding XYmath source code, do the following::

    cd full/path/to/xymath
    pip install -e .
    
        OR on Linux
    sudo pip install -e .
        OR perhaps
    pip install --user -e .
    
This will execute the local ``setup.py`` file and insure that the pip-specific commands in ``setup.py`` are run.

Running XYmath
--------------

There are several ways to run XYmath
    
    #. Launch the GUI, enter and fit data and perhaps run some math operations
    #. Write a script to launch the GUI with data (see :ref:`internal_examples`)
    #. Run a script that outputs to the console (see :ref:`internal_examples`)

.. _internal_launch_gui:

Launch GUI
~~~~~~~~~~
    
After installing with ``pip``, there will be a launch command line program called **xymath** or, on Windows, **xymath.exe** installed on your system. From a terminal or command prompt window simply type::

    xymath
    
      OR
      
    xymath <dataset name>

and XYmath will start. If a dataset name is given (e.g. mydata.x_y) then XYmath will look for the dataset and load it upon launch.  For example::

    xymath mydata
    xymath mydata.x_y
    xymath C:\long\path\to\sample\data\mydata
    xymath ~/xy_data/mydata.x_y
    


If XYmath does not start with the above command, then there may be an issue with your system path.
The path for the xymath executable might be something like::

    /usr/local/bin/xymath             (if installed with sudo pip install -e .)
         or 
    /home/<user>/.local/bin/xymath    (if installed with pip install -e .)
         or 
    C:\Python27\Scripts\xymath.exe    (on Windows)

Make sure your system path includes the above path to **xymath**.


.. _internal_pip_error:

pip Error Messages
------------------

If you get an error message that ``pip`` is not found, see `<https://pip.pypa.io/en/latest/installing.html>`_ for full description of ``pip`` installation.

There might be issues with ``pip`` failing on Linux with a message like::


    InsecurePlatformWarning
            or    
    Cannot fetch index base URL https://pypi.python.org/simple/

Certain Python platforms (specifically, versions of Python earlier than 2.7.9) have the InsecurePlatformWarning. If you encounter this warning, it is strongly recommended you upgrade to a newer Python version, or that you use pyOpenSSL.    

Also ``pip`` may be mis-configured and point to the wrong PyPI repository.
You need to fix this global problem with ``pip`` just to make python usable on your system.


If you give up on upgrading python or fixing ``pip``, 
you might also try downloading the xymath source package 
(and all dependency source packages)
from PyPI and installing from source as shown above at :ref:`internal_source_install`


