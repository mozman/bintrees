#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test binary trees
# Created: 28.04.2010

import unittest

if sys.platform.startswith('linux2'):
    import pyximport
    pyximport.install()

from tree_test import TestAbstTree
from bintrees.ctrees import cRBTree

class TestcRBTree(TestAbstTree):
    def setUp(self):
        self.TREE = cRBTree

if __name__=='__main__':
    unittest.main()