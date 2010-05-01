#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test RBTrees
# Created: 28.04.2010

import unittest

from tree_test import TestAbstTree
from bintrees.rbtree import RBTree

class TestRBTree(TestAbstTree):
    @property
    def TREE(self):
        return RBTree

if __name__=='__main__':
    unittest.main()