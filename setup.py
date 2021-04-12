import setuptools

import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cmdline_provenance',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A Python package for keeping track of your data processing steps',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Damien Irving',
    author_email='irving.damien@gmail.com',
    url='https://github.com/DamienIrving/cmdline_provenance',
    packages=['cmdline_provenance'],
    zip_safe=False,
    install_requires=['ipynbname'],
    license='MIT License',
    include_package_data=True,
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',)
)
