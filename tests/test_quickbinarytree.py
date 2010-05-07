#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test quick binary trees
# Created:07.05.2010
import sys
sys.path.append('d:\user\python\bintrees')

import unittest
from tree_test import CheckTree

from bintrees import QuickBinaryTree

class TestQuickBinaryTree(CheckTree, unittest.TestCase):
    @property
    def TREE(self):
        return QuickBinaryTree

if __name__=='__main__':
    unittest.main()