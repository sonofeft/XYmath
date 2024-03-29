"""
The ``_version.py`` file can be executed with execfile to create a local variable __version__::

    execfile('_version.py')             # python 2.x
    exec(open('_version.py').read())    # python 3.x

creates local __version__ variable.  

Used to set version info throughout the project.

------
"""
__version__ = '0.3.1'  # METADATA_RESET:__version__ = '<<version>>'
