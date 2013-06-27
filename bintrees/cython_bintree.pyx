#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython unbalanced binary tree module
# Created: 28.04.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

__all__ = ['cBinaryTree']

from .abctree import ABCTree

from .cython_basetree cimport _BaseTree
from .ctrees cimport ct_bintree_insert, ct_bintree_remove


cdef class _BinaryTree(_BaseTree):
    def insert(self, key, value):
        res = ct_bintree_insert(&self._root, key, value)
        if res < 0:
            raise MemoryError('Can not allocate memory for node structure.')
        self._count += res

    def remove(self, key):
        cdef int result
        result = ct_bintree_remove(&self._root, key)
        if result == 0:
            raise KeyError(str(key))
        else:
            self._count -= 1

class FastBinaryTree(_BinaryTree, ABCTree):
    pass