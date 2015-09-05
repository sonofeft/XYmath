"""A setuptools based setup module for XYmath

See:
http://xymath.readthedocs.org/en/latest/
https://github.com/sonofeft/XYmath

If installing from source, then
the best way to install XYmath is to use pip after navigating to the source directory::

    cd <path to where setup.py is located>
    pip install -e .

This will execute the setup.py file and insure that its pip-specific commands are run.

"""


# Always prefer setuptools over distutils
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# To use a consistent encoding
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    # Place install_requires into the text file "requirements.txt"
    with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f2:
        requires = f2.read().strip().splitlines()
else:
    requires = ['mock']

target_file = os.path.join( here, 'xymath','_version.py')
exec( open( target_file ).read() )  # creates local __version__ variable


setup(
    name='xymath',
    version = __version__,  # METADATA_RESET:    version = '<<version>>',

    description = 'A GUI and API that creates, documents and explores y=f(x) curve fits',
    long_description = long_description,

    # The project's main homepage.
    url='http://xymath.readthedocs.org/en/latest/',
    download_url='https://github.com/sonofeft/XYmath',

    # Author details
    author = 'Charlie Taylor',
    author_email = 'charlietaylor@users.sourceforge.net',

    # license
    license = 'GPL-3',

    classifiers = [
        # Common status values are: "3 - Alpha", "4 - Beta", "5 - Production/Stable"
        'Development Status :: 4 - Beta',

        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        "Intended Audience :: End Users/Desktop",
        'Topic :: Software Development :: Build Tools',

        # This license should match "license" above
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    platforms = 'any',

    # What does your project relate to?
    keywords = 'xymath setuptools development',

    packages = find_packages(exclude=['.tox', '.hg', 'docs']),
    package_data = {'xymath':['gui/*.ico',]},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed.
    install_requires = requires,  # read from requirements.txt

    tests_require = ['nose','coverage'], # ...OR... ['pytest','pytest-cov']
    test_suite='xymath.tests', # allows "setup.py test" to work

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    zip_safe= False,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.

    entry_points = {
        'console_scripts': [
            'xymath=xymath.gui.xygui:main',
        ],
    },
)