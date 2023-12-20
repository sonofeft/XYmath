
python  -m pip install --upgrade twine

python  -m pip install --upgrade build

python setup.py sdist bdist_wheel

twine upload --skip-existing dist/*

rem use:  twine check dist/*  OR twine check dist/*24.tar.gz (where: 24 is current version)

rem python -m build

rem python  -m twine upload dist/* --verbose --config-file "%HOMEPATh%\.pypirc"

rem if long description fails, enter the following
rem use:  twine check dist/*  OR twine check dist/*24.tar.gz (where: 24 is current version)


