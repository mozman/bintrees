#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython unbalanced binary tree module
# Created: 28.04.2010

__all__ = ['cBinaryTree2']

cdef extern from "python.h":
    ctypedef struct PyObject:
        pass

cdef extern from "node.h":
    ctypedef struct node_t:
        node_t *link[2]
        PyObject *key
        PyObject *value



    node_t *node_new(object key, object value)
    void node_delete(node_t *node)
    object node_get_key(node_t *node)
    object node_get_value(node_t *node)
    void node_set_value(node_t*, object value)
    void tree_clear(node_t *node)
    void node_swap_data(node_t *node1, node_t *node2)


cdef class Node:
    # interface object for TreeMixin, only read access from Python
    cdef node_t *cnode

    def __cinit__(self):
        self.cnode = NULL

    @property
    def key(self):
        # return value as python object
        return node_get_key(self.cnode)

    @property
    def value(self):
        # return value as python object
        return node_get_value(self.cnode)

    @property
    def left(self):
        # return the left child as python object
        return from_node_t(self.cnode.link[0])

    @property
    def right(self):
        # return the right child as python object
        return from_node_t(self.cnode.link[1])

    def __getitem__(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        return from_node_t(self.cnode.link[key])

    def free(self):
        pass # contains no python data

cdef object from_node_t(node_t *node):
        cdef Node new_node
        new_node = Node()
        new_node.cnode = node
        return new_node

cdef class cBinaryTree2:
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
        cdef Node node
        if self._root == NULL:
            return None
        else:
            node = Node()
            node.cnode = self._root
            return node

    @property
    def compare(self):
        return self._compare

    @property
    def count(self):
        return self._count

    cdef node_t *new_node(self, key, value):
        """Create a new tree node."""
        self._count += 1
        return node_new(key, value)

    def clear(self):
        tree_clear(self._root)
        self._count = 0
        self._root = NULL

    def find_node(self, key):
        cdef int cval
        cdef node_t *node
        node = self._root
        while node != NULL:
            cval = <int>self._compare(key, node_get_key(node))
            if cval == 0:
                return from_node_t(node)
            elif cval < 0:
                node = node.link[0]
            else:
                node = node.link[1]
        return None

    def insert(self, key, value):
        cdef node_t *parent, *node
        cdef int direction, cval

        if self._root == NULL:
            self._root = self.new_node(key, value)
        else:
            compare = self._compare
            direction = 0
            parent = NULL
            node = self._root
            while True:
                if node == NULL:
                    parent.link[direction] = self.new_node(key, value)
                    break
                cval = <int> compare(key, node_get_key(node))
                if cval == 0: # key exists
                    node_set_value(node, value)
                    break
                else:
                    parent = node
                    direction = 0 if cval < 0 else 1
                    node = node.link[direction]

    def remove(self, key):
        cdef node_t *node, *parent, *replacement
        cdef int direction, cmp_res, down_dir

        node = self._root
        if node == NULL:
            raise KeyError(str(key))
        else:
            compare = self._compare
            parent = NULL
            direction = 0
            while True:
                cmp_res = <int> compare(key, node_get_key(node))
                if cmp_res == 0:
                    # remove node
                    if (node.link[0] != NULL) and (node.link[1] != NULL):
                        # find replacment node: smallest key in right-subtree
                        parent = node
                        direction = 1
                        replacement = node.link[1]
                        while replacement.link[0] != NULL:
                            parent = replacement
                            direction = 0
                            replacement = replacement.link[0]
                        parent.link[direction] = replacement.link[1]
                        #swap places
                        node_swap_data(node, replacement)
                        node = replacement # delete replacement node
                    else:
                        down_dir = 1 if node.link[0] == NULL else 0
                        if parent == NULL: # root
                            self._root = node.link[down_dir]
                        else:
                            parent.link[direction] = node.link[down_dir]
                    node_delete(node)
                    self._count -= 1
                    break
                else:
                    direction = 0 if cmp_res < 0 else 1
                    parent = node
                    node = node.link[direction]
                    if node == NULL:
                        raise KeyError(str(key))

