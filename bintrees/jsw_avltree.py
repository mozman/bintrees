#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: avl tree module (Julienne Walker Top-down algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_avl.aspx
# Created: 01.05.2010

from basetree import BaseTree

__all__ = ['JSWAVLTree']

class Node(object):
    __slots__ = ['key', 'value', 'color', 'left', 'right']
    def __init__(self, key, value, color):
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None

    def free(self):
        self.left = None
        self.right = None
        self.key = None
        self.value = None

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

class JSWAVLTree(BaseTree):
    def copy(self):
        return JSWAVLTree(self) # has no problem with sorted keys
    __copy__ = copy

    def new_node(self, key, value, color):
        self._count += 1
        return Node(key, value, color)

    def insert(self, key, value):
        pass

    def remove(self, key):
        pass
