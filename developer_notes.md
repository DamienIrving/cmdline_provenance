## Developer notes

Packaging for [PyPI](https://pypi.org/project/cmdline-provenance/)
was done following the [official instructions](https://packaging.python.org/tutorials/packaging-projects/)
as well as [this guide](http://python-packaging.readthedocs.io/en/latest/minimal.html) on minimal package requirements.

The [conda-forge](https://anaconda.org/conda-forge/cmdline_provenance) recipe was created following the
[offical instructions](https://conda-forge.org/docs/maintainer/adding_pkgs.html#step-by-step-instructions).

The [documentation](https://cmdline-provenance.readthedocs.io/en/latest/) was created using Sphinx and ReadTheDocs,
following [these instructions](http://dont-be-afraid-to-commit.readthedocs.io/en/latest/documentation.html).

To re-build and submit a new version to PyPI and conda-forge:

0. Create a test environment to work in:
```
$ conda create -n test pip twine
$ conda activate test
```
1. Increment the version number in `setup.py`
2. Install the package and each the everything works correctly:
```
$ pip install -e .
```
3. Create the source distribution and wheels:
```
$ python setup.py sdist bdist_wheel
```
4. Remove the old versions from `dist/`
5. Upload to [TestPyPI](https://test.pypi.org/project/cmdline-provenance/) to check that everything looks fine
```
$ twine upload --repository testpypi dist/*`
```
5. Upload to PyPI
```
$ twine upload dist/*`
```
6. Fork the [conda feedstock repo](https://github.com/conda-forge/cmdline_provenance-feedstock), make necessary changes to `recipe/meta.yaml` and then submit a PR.
