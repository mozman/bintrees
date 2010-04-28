# to build c-extension:
# setup.py build_ext --inplace

import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("bintrees.cbintree", ["bintrees/cbintree.pyx"]),
               Extension("bintrees.cavltree", ["bintrees/cavltree.pyx"]),
               Extension("bintrees.crbtree", ["bintrees/crbtree.pyx"]), ]

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'bintrees',
    version='0.1.0',
    description='Package provides Binary-, RedBlack- and AVL-Trees in Python and Cython.',
    author='mozman',
    url='http://bitbucket.org/mozman/bintrees',
    author_email='mozman@gmx.at',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
    packages=['bintrees'],
    requires=['cython'],
    long_description=read('README.txt'),
    platforms="OS Independent",
    license="GPLv3",
    classifiers=[
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.6",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
