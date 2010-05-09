#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test quick rb trees
# Created: 09.05.2010
import sys

import unittest

from tree_test import CheckTree
from bintrees import QuickAVLTree

class TestQuickAVLTree(CheckTree, unittest.TestCase):
    @property
    def TREE(self):
        return QuickAVLTree

if __name__=='__main__':
    unittest.main()