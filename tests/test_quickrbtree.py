#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test quick rb trees
# Created: 09.05.2010
import sys
sys.path.append('d:\user\python\bintrees')

import unittest
from tree_test import CheckTree

from bintrees import QuickRBTree

class TestQuickRBTree(CheckTree, unittest.TestCase):
    @property
    def TREE(self):
        return QuickRBTree

if __name__=='__main__':
    unittest.main()