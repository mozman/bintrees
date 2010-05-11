#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython unbalanced binary tree module
# Created: 28.04.2010

__all__ = ['cAVLTree']

from cwalker import cWalker

from cwalker cimport *
from ctrees cimport *

cdef class cAVLTree:
    cdef node_t *_root
    cdef int _count
    cdef object _compare

    def __cinit__(self, items=None, compare=None):
        self._root = NULL
        self._compare = compare # if compare is None use PyObject_compare()
        self._count = 0
        if items:
            self.update(items)

    def __dealloc__(self):
        ct_delete_tree(self._root)

    @property
    def compare(self):
        return self._compare if self._compare is not None else cmp

    @property
    def count(self):
        return self._count

    def __getstate__(self):
        data = dict(self.iteritems())
        return {'data': data, 'cmp': self._compare}

    def __setstate__(self, state):
        self._compare = state['cmp']
        self.update(state['data'])

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
        res = avl_insert(&self._root, key, value, self._compare)
        if res < 0:
            raise MemoryError('Can not allocate memory for node structure.')
        else:
            self._count += res

    def remove(self, key):
        cdef int result
        result =  avl_remove(&self._root, key, self._compare)
        if result == 0:
            raise KeyError(str(key))
        else:
            self._count -= 1

    def max_item(self):
        """ Get item with max key of tree, raises ValueError if tree is empty. """
        cdef node_t *node
        node = ct_max_node(self._root)
        if node == NULL: # root is None
            raise ValueError("Tree is empty")
        return (<object>node.key, <object>node.value)

    def min_item(self):
        """ Get item with min key of tree, raises ValueError if tree is empty. """
        cdef node_t *node
        node = ct_min_node(self._root)
        if node == NULL: # root is None
            raise ValueError("Tree is empty")
        return (<object>node.key, <object>node.value)

    def index(self, key):
        """ T.index(k) -> index, raises KeyError if k not in T """
        cdef int result
        result = ct_index_of(self._root, key, self._compare)
        if result >= 0:
            return result
        else:
            raise KeyError(str(key))

    def item_at(self, index):
        """ T.item_at(index) -> item (k,v) """
        cdef node_t *result
        cdef int n
        n = <int> index
        if n < 0:
            n = self._count + n
        if (n < 0) or (n >= self._count):
            raise IndexError('item_at()')
        result = ct_node_at(self._root, n)
        if result == NULL:
            # index is in valid range so NULL should not be returned,
            # implementation error in ct_node_at(...) function!
            raise SystemError('got NULL from ct_node_at(...)')
        else:
            return (<object>result.key, <object>result.value)

