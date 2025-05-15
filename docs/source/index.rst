.. SpecPiNK documentation master file, created by
   sphinx-quickstart on Thu May 15 19:25:41 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

specpink - Spectroscopic Data Reduction
=======================================

Welcome to the documentation for **specpink**, a Python package for reducing and calibrating spectroscopic data from the
Nordkuppel telescope using FITS files.

This package provides tools for:
- Creating master calibration frames from raw exposures
- Applying bias/dark/flat corrections
- Extracting and calibrating 1D spectra
- Saving processed results to FITS files

.. note::

   This documentation is still under development. Please refer to the source code for the most up-to-date functionality.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Modules

   calibrator
   reducer
   utils
   spectrum
   pipeline
   main

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`