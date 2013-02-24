#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

# to build c-extension:
# setup.py build_ext --inplace --force

import os
from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
    ext_modules = [Extension("bintrees.cwalker", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/cwalker.pyx"]),
                   Extension("bintrees.qbintree", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/qbintree.pyx"]),
                   Extension("bintrees.qrbtree", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/qrbtree.pyx"]),
                   Extension("bintrees.qavltree", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/qavltree.pyx"]),
                   ]
    commands = {'build_ext': build_ext}
except ImportError:
    ext_modules = []
    commands = {}


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='bintrees',
    version='1.0.1',
    description='Package provides Binary-, RedBlack- and AVL-Trees in Python and Cython.',
    author='mozman',
    url='http://bitbucket.org/mozman/bintrees',
    download_url='http://bitbucket.org/mozman/bintrees/downloads',
    author_email='mozman@gmx.at',
    cmdclass=commands,
    ext_modules=ext_modules,
    packages=['bintrees'],
    long_description=read('README.txt'),
    platforms="OS Independent",
    license="MIT License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Cython",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: IronPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
