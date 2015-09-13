.. 2015-09-13 sonofeft 302bc9d1a23b9596ac9cb12f02924a71960a3e89
   Maintain spacing of "History" and "GitHub Log" titles

History
=======

GitHub Log
----------

* Sep 13, 2015
    - (by: sonofeft) 
        - Added more examples
* Sep 12, 2015
    - (by: sonofeft) 
        - Version 0.2.1
            Added docs for Calibration Example
            Changed sign of error plots
            Added matplotlib to console examples
* Sep 11, 2015
    - (by: sonofeft) 
        - Calibration Example
            Also fixed linear_fitL between simple and exhaustive fits
* Sep 10, 2015
    - (by: sonofeft) 
        - Added examples
            Both GUI and console examples added.
            Updated GUI to accept non-linear eqns with initial const guesses
* Sep 09, 2015
    - (by: sonofeft) 
        - Added Error Plots
            Added start of Patmos Example
* Sep 08, 2015
    - (by: sonofeft) 
        - Version 0.1.9
            Code improvements and history update
        - code upgrades and fixes
            Added launch GUI from script
            Changed x==None statements to x is None
            Fixed matplotlib figure.max_open_warning
            Made XY_Job.define_dataset tolerant of list inputs instead of numpy
            arrays
* Sep 07, 2015
    - (by: sonofeft) 
        - upgrade docs
        - added upgrade page
        - curve fit docs update
        - add images for history page
        - Lots of documentation additions
* Sep 06, 2015
    - (by: sonofeft) 
        - Added doc warning for python3 imaging-tk
        - Changed logo to orange POV-based PNG
        - Changed logo to POV-based PNG
        - Version 0.1.8, Making xymath/examples subdir install
        - Version 0.1.7,  Removed mbcs coding specifier
        - Removed make_toctree from fulltoc.py
* Sep 05, 2015
    - (by: sonofeft) 
        - Updated HISTORY.rst file

* Sep 05, 2015
    - (by: sonofeft) 
        - Give up on functions.rst (i.e. a full build on ReadTheDocs)
        - Give functions.rst a last chance
        - That's it, I'm giving up on a full build at ReadTheDocs
        - Kitchen Sink Docs attempt
        - fixed import bug in setup.py
        - added mock logic to setup.py
        - move requirements.txt into setup.py
        - add freetype an png to requirements.txt
        - try removing install_requires in setup.py
        - try again for matplotlib version
        - try matplotlib v 1.5
        - try the new dev version of matplotlib
        - try older version of matplotlib
        - trying matplotlib-dev
        - put RTD mock logic into conf.py
        - made pillow a requirement
        - Try including imaging-tk in requirements for ReadTheDocs
        - removed genindex from index.rst
        - Removed sphinx.ext.autodoc from conf.py
            Removed from:
            extensions = [
            'sphinx.ext.autodoc',
            'sphinx.ext.intersphinx',
            'sphinx.ext.todo',
            'sphinx.ext.ifconfig',
            'fulltoc'
            ]
        - Removed mock logic
        - added some mock logic to setup.py
        - Removed functions.rst file
        - Omit functions.rst from index.rst
        - Fixed mock logic
        - Shot in the dark with python version
        - added json to mock
        - change to mock modules for readthedocs
        - Use "READTHEDOCS" in setup.py to mock requirements
        - need "mock" module in readthedocs_requirements.txt
        - Added ReadTheDocs only requirements file
