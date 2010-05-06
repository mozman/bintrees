#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test RBTrees
# Created: 28.04.2010

import unittest
from tree_test import CheckTree

from bintrees import FastRBTree

class TestFastRBTree(CheckTree, unittest.TestCase):
    @property
    def TREE(self):
        return FastRBTree

if __name__=='__main__':
    unittest.main()