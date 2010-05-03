#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: binary trees package
# Created: 03.05.2010

from treemixin import TreeMixin
from bintree import BinaryTree
from avltree import AVLTree
from rbtree import RBTree
from cbintree import cBinaryTree
from cavltree import cAVLTree
from crbtree import cRBTree

__all__ = ['FastBinaryTree', 'FastAVLTree', 'FastRBTree',
           'BinaryTree', 'AVLTree', 'RBTree']

class FastBinaryTree(cBinaryTree, TreeMixin):
    pass

class FastAVLTree(cAVLTree, TreeMixin):
    pass

class FastRBTree(cRBTree, TreeMixin):
    pass
