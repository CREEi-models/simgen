# Steps for creating package

### make sure setuptools up to date:
    python3 -m pip install --user --upgrade setuptools wheel
### create package for distribution
python3 setup.py sdist bdist_wheel
### upgrade twine (not necessary each time)
python3 -m pip install --user --upgrade twine
### upload (our site is on https://test.pypi.org/project/creei-compas/0.0.1/)
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
Will be asked for username: enter __token__ and then paste the following token as password. 
pypi-AgENdGVzdC5weXBpLm9yZwIkODAzNzc5ZDYtNWEzNC00MGU0LWFlMzQtNmQ4M2EyY2Q0OTkyAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiABXXIoCihMX57AvuByaApZsVNKlzMp_jhq1PX7Lca2fA

### To install on any computer: 
pip install -i https://test.pypi.org/simple/ creei-compas==0.0.1
