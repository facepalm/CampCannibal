#! /usr/bin/env python

import sys
import os
from glob import glob
import sys

if sys.platform == 'win32':
    #Supress warnings in error log for py2exe
    import warnings
    warnings.filterwarnings('ignore')

import zipfile
import md5

import pyglet

try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    sys.path.insert(0, libdir)

try:
    import lepton
except ImportError:
    pass

import main
main.main()

