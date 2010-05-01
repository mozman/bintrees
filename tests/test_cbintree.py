#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test cython binary trees
# Created: 28.04.2010
import sys
import unittest

if sys.platform.startswith('linux2'):
    import pyximport
    pyximport.install()

from tree_test import TestAbstTree
from bintrees.ctrees import cBinaryTree

class TestcBinaryTree(TestAbstTree):
    @property
    def TREE(self):
        return cBinaryTree

if __name__=='__main__':
    unittest.main()