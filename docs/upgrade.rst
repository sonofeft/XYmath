
.. upgrade

Upgrade XYmath
============

.. _Python(x,y): http://python-xy.github.io/
.. _Anaconda: https://store.continuum.io/cshop/anaconda/

.. _Unofficial Windows Binaries for Python Extension Packages: http://www.lfd.uci.edu/~gohlke/pythonlibs/

While XYmath is under development, there may well be occasion to upgrade to a newer version.

I **Strongly Recommend** using::
    
    pip uninstall xymath
        <followed by>
    pip install xymath

.. warning::
    **Do NOT Use**::
    
    pip install --upgrade xymath
    
Using the --upgrade flag will initiate attempts to upgrade scipy, numpy and matplotlib which will fail if your system is not properly configured.

On my systems, the rollback of the attempts to upgrade those packages did not work and I was forced to reinstall them.

If using Anaconda_, they can be restored as::
    
    conda install numpy
    conda install numexpr
    conda install scipy
    conda install matplotlib
    
If using `Python(x,y)`_, the best approach would be to download install EXE files from `Unofficial Windows Binaries for Python Extension Packages`_
