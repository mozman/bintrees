#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython unbalanced binary tree module
# Created: 28.04.2010

__all__ = ['cBinaryTree']

cdef extern from "python.h":
    ctypedef struct PyObject:
        pass

cdef extern from "ctrees.h":
    ctypedef struct node_t:
        node_t *link[2]
        PyObject *key
        PyObject *value

    object ct_get_key(node_t *node)
    object ct_get_value(node_t *node)
    void ct_delete_tree(node_t *root)
    node_t *ct_find_node(node_t *root, object key, object cmp)
    node_t *ct_bintree_insert(node_t *root, object key, object value, object cmp)
    node_t *ct_bintree_remove(node_t *root, object key, object cmp)

cdef class TempNode:
    # temporary object for TreeMixin, only read access from Python
    cdef node_t *ct_node

    def __cinit__(self):
        self.ct_node = NULL

    @property
    def key(self):
        # return value as python object
        return ct_get_key(self.ct_node)

    @property
    def value(self):
        # return value as python object
        return ct_get_value(self.ct_node)

    @property
    def left(self):
        # return the left child as python object
        return from_node_t(self.ct_node.link[0])

    @property
    def right(self):
        # return the right child as python object
        return from_node_t(self.ct_node.link[1])

    def __getitem__(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        return from_node_t(self.ct_node.link[key])

    def free(self):
        pass # contains no python data

cdef object from_node_t(node_t *node):
        cdef TempNode new_node
        if node != NULL:
            new_node = TempNode()
            new_node.ct_node = node
        else:
            new_node = None
        return new_node

cdef class cBinaryTree:
    cdef node_t *_root
    cdef int _count
    cdef object _compare

    def __init__(self, items=[], compare=None):
        self._root = NULL
        self._compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    @property
    def root(self):
        cdef TempNode node
        if self._root == NULL:
            return None
        else:
            return from_node_t(self._root)

    @property
    def compare(self):
        return self._compare

    @property
    def count(self):
        return self._count

    def clear(self):
        ct_delete_tree(self._root)
        self._count = 0
        self._root = NULL

    def find_node(self, key):
        cdef node_t *node
        node = ct_find_node(self._root, key, self._compare)
        if node == NULL:
            return None
        else:
            return from_node_t(node)

    def insert(self, key, value):
        self._root = ct_bintree_insert(self._root, key, value, self._compare)

    def remove(self, key):
        cdef node_t *result
        result = ct_bintree_remove(self._root, key, self._compare)
        if result == NULL:
            raise KeyError(str(key))
        else:
            self._root = result

