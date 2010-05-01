#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test JSWRBTrees
# Created: 28.04.2010

import unittest

from tree_test import TestAbstTree
from bintrees.jsw_rbtree import JSWRBTree

class TestJSWRBTree(TestAbstTree):
    def setUp(self):
        self.TREE = JSWRBTree

if __name__=='__main__':
    unittest.main()