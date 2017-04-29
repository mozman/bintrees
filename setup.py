#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

# `python setup.py install` should build the C extension if you have Cython

import os
from setuptools import setup
from setuptools import Extension

try:
    from Cython.Distutils import build_ext
    ext_modules = [Extension("bintrees.cython_trees", ["bintrees/ctrees.c", "bintrees/cython_trees.pyx"]),
                   ]
    commands = {'build_ext': build_ext}
except ImportError:
    ext_modules = []
    commands = {}


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='bintrees',
    version='2.0.7',
    description='Package provides Binary-, RedBlack- and AVL-Trees in Python and Cython.',
    author='mozman',
    url='https://github.com/mozman/bintrees.git',
    download_url='https://github.com/mozman/bintrees/releases',
    author_email='mozman@gmx.at',
    cmdclass=commands,
    ext_modules=ext_modules,
    packages=['bintrees'],
    long_description=read('README.rst')+read('NEWS.rst'),
    platforms="OS Independent",
    license="MIT License",
    classifiers=[
        "Development Status :: 6 - Mature",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Cython",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
