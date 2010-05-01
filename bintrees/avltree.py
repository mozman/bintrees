#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: avl tree module (Julienne Walker Top-down algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_avl.aspx
# Created: 01.05.2010

from basetree import BaseTree

__all__ = ['AVLTree']

AVL_LEFT = 0
AVL_RIGHT = 1

class Node(object):
    __slots__ = ['left', 'right', 'parent', 'height', 'key', 'value']

    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.balance = 0

    def __getitem__(self, key):
        """Get left or right node by index"""
        if key == 0:
            return self.left
        elif key == 1:
            return self.right
        else:
            raise KeyError(str(key))

    def __setitem__(self, key, value):
        """Set left or right node by index"""
        if key == 0:
            self.left = value
        elif key == 1:
            self.right = value
        else:
            raise KeyError(str(key))

    def free(self):
        """Remove all references."""
        self.left = None
        self.right = None
        self.key = None
        self.value = None

def jsw_single(root, direction):
    save = root[1-direction]
    root[1-direction] = save[direction]
    save[direction] = root
    return save

class AVLTree(BaseTree):
    """AVL Tree (balanced binary search tree)

    The AVL tree structure is a balanced binary tree which stores a collection of
    nodes.  Each node has a key and a value associated with it.  The nodes are
    sorted within the tree based on the order of their keys. Modifications to the
    tree are constructed such that the tree remains balanced at all times (there are
    always roughly equal numbers of nodes on either side of the tree).

    Balanced binary trees have several uses.  They can be used as a mapping
    (searching for a value based on its key), or as a set of keys which is always
    ordered.
    """
    def copy(self):
        """Returns a shallow copy of this tree"""
        return AVLTree(self) # has no problem with sorted keys
    __copy__ = copy
    def new_node(self, key, value):
        return Node(key, value)
