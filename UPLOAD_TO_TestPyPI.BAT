
python  -m pip install --upgrade build

python -m build

python  -m pip install --upgrade twine

python  -m twine upload --verbose --repository testpypi dist/* --config-file "%HOMEPATh%\.pypirc"

rem install as:  pip install -i https://test.pypi.org/simple/ parasol

rem if long description fails, enter the following
rem use:  twine check dist/*  OR twine check dist/*24.tar.gz (where: 24 is current version)
