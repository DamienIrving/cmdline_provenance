## Developer notes

Packaging for PyPI was done following the [official instructions](https://packaging.python.org/tutorials/packaging-projects/)
as well as [this guide](http://python-packaging.readthedocs.io/en/latest/minimal.html) on minimal package requirements.

The documentation was created using Sphinx and ReadTheDocs,
following [these instructions](http://dont-be-afraid-to-commit.readthedocs.io/en/latest/documentation.html).

To re-build and submit a new version to [PyPI](https://pypi.org/project/cmdline-provenance/):

1. Increment the version number in `setup.py`
2. `$ python setup.py sdist bdist_wheel`
3. Remove the old versions from `dist/`
4. `$ /Users/irv033/.local/bin/twine upload dist/*`

