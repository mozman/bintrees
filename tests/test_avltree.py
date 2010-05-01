#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test AVLTrees
# Created: 28.04.2010

import unittest

from tree_test import TestAbstTree
from bintrees.avltree import AVLTree

class TestAVLTree(TestAbstTree):
    @property
    def TREE(self):
        return AVLTree

if __name__=='__main__':
    unittest.main()