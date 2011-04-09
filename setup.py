#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# to build c-extension:
# setup.py build_ext --inplace --force

import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("bintrees.cwalker", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/cwalker.pyx"]),
               Extension("bintrees.qbintree", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/qbintree.pyx"]),
               Extension("bintrees.qrbtree", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/qrbtree.pyx"]),
               Extension("bintrees.qavltree", ["bintrees/ctrees.c", "bintrees/stack.c", "bintrees/qavltree.pyx"]),
               ]
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'bintrees',
    version='0.4.0',
    description='Package provides Binary-, RedBlack- and AVL-Trees in Python and Cython.',
    author='mozman',
    url='http://bitbucket.org/mozman/bintrees',
    download_url='http://bitbucket.org/mozman/bintrees/downloads',
    author_email='mozman@gmx.at',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
    packages=['bintrees'],
    long_description=read('README.txt'),
    platforms="OS Independent",
    license="GPLv3",
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Cython",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
