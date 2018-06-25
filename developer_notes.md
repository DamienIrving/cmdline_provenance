## Developer notes

Packaging for PyPI was done following the [official instructions](https://packaging.python.org/tutorials/packaging-projects/)
as well as [this guide](http://python-packaging.readthedocs.io/en/latest/minimal.html) on minimal package requirements.

To re-build and submit a new version to PyPI:
```
$ python setup.py sdist bdist_wheel
$ /Users/irv033/.local/bin/twine upload dist/*
```

The documentation was created using Sphinx and ReadTheDocs,
following [these instructions](http://dont-be-afraid-to-commit.readthedocs.io/en/latest/documentation.html).

