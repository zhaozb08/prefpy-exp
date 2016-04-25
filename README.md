PrefPy-experiments
===============

Scripts for experiments using PrefPy (found at https://github.com/xialirong/prefpy)

This code has been split off of the original PrefPy package/repository in an effort to organize and remove code not part of the implementations of the algorithms in PrefPy.  All tests and experiments are now located here.


Work In Progress
================

- The code in this repository is research code, so it is constantly in a state of change
- The imports must all be changed as these files were originally part of the PrefPy package itself and now rely on it being installed separately


Installation
========

- Use of MATLAB optimization in this package requires Python 3.4 due to lack of support yet for Python 3.5 by the MATLAB Engine

Install by running setup.py with Python 3.4 (or greater) with the command

    python3 setup.py install

Symlink install while developing to keep changes in the code instead with the command

    python3 setup.py develop