from setuptools import setup

setup(
    name='cmdline_provenance',
    version='0.1.0',
    description='Utilities for capturing the history of commands used to produce a given output',
    author='Damien Irving',
    author_email='irving.damien@gmail.com',
    url='https://github.com/DamienIrving/cmdline_provenance',
    packages=['cmdline_provenance'],
    zip_safe=False,
    install_requires=['datetime', 'gitpython'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',)
)

# 