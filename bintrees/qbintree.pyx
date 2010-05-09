#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython unbalanced binary tree module
# Created: 28.04.2010

__all__ = ['cQBinaryTree']

from cwalker import cWalker

from cwalker cimport *
from ctrees cimport *

cdef class cQBinaryTree:
    cdef node_t *_root
    cdef int _count
    cdef object _compare

    def __init__(self, items=[], compare=None):
        self._root = NULL
        #self._compare = compare if compare is not None else cmp
        self._compare = compare # if compare is None use PyObject_compare()
        self._count = 0
        self.update(items)

    @property
    def compare(self):
        return self._compare if self._compare is not None else cmp

    @property
    def count(self):
        return self._count

    def clear(self):
        ct_delete_tree(self._root)
        self._count = 0
        self._root = NULL

    def get_value(self, key):
        result = <object> ct_get_item(self._root, key, self._compare)
        if result is None:
            raise KeyError(key)
        else:
            return result[1]

    def get_walker(self):
        cdef cWalker walker
        walker = cWalker()
        walker.set_tree(self._root, self._compare)
        return walker

    def insert(self, key, value):
        res = ct_bintree_insert(&self._root, key, value, self._compare)
        if res < 0:
            raise MemoryError('Can not allocate memory for node structure.')
        self._count += res

    def remove(self, key):
        cdef int result
        result =  ct_bintree_remove(&self._root, key, self._compare)
        if result == 0:
            raise KeyError(str(key))
        else:
            self._count -= 1

