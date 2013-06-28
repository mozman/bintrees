#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: Binary trees implemented in Cython/C
# Created: 28.04.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

from .abctree import _ABCTree
from ctrees cimport *
from stack cimport *


cdef node_t* get_leaf_node(node_t *node):
    """ get a leaf node """
    while True:
        if node.link[0] != NULL:
            node = node.link[0]
        elif node.link[1] != NULL:
            node = node.link[1]
        else:
            return node


cdef class _BaseTree:
    cdef node_t *root
    cdef int _count

    def __cinit__(self, items=None):
        self.root = NULL
        self._count = 0
        if items is not None:
            self.update(items)

    def __dealloc__(self):
        ct_delete_tree(self.root)
        self._count = 0
        self.root = NULL

    @property
    def count(self):
        return self._count

    def __getstate__(self):
        return dict(self.items())

    def __setstate__(self, state):
        self.update(state)

    def clear(self):
        ct_delete_tree(self.root)
        self._count = 0
        self.root = NULL

    def get_value(self, key):
        result = <object> ct_get_item(self.root, key)
        if result is None:
            raise KeyError(key)
        else:
            return result[1]

    def max_item(self):
        """ Get item with max key of tree, raises ValueError if tree is empty. """
        cdef node_t *node = ct_max_node(self.root)
        if node == NULL: # root is None
            raise ValueError("Tree is empty")
        return <object>node.key, <object>node.value

    def min_item(self):
        """ Get item with min key of tree, raises ValueError if tree is empty. """
        cdef node_t *node = ct_min_node(self.root)
        if node == NULL: # root is None
            raise ValueError("Tree is empty")
        return <object>node.key, <object>node.value

    cpdef succ_item(self, key):
        """ Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist.
        """
        cdef node_t *node = ct_succ_node(self.root, key)
        if node == NULL: # given key is biggest in tree
            raise KeyError(str(key))
        return <object> node.key, <object> node.value

    def prev_item(self, key):
        """ Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist.
        """
        cdef node_t *node = ct_prev_node(self.root, key)
        if node == NULL: # given key is smallest in tree
            raise KeyError(str(key))
        return <object> node.key, <object> node.value

    def floor_item(self, key):
        """ Get the element (k,v) pair associated with the greatest key less
        than or equal to the given key, raises KeyError if there is no such key.
        """
        cdef node_t *node = ct_floor_node(self.root, key)
        if node == NULL:  # given key is smaller than min-key in tree
            raise KeyError(str(key))
        return <object> node.key, <object> node.value

    def ceiling_item(self, key):
        """ Get the element (k,v) pair associated with the smallest key greater
        than or equal to the given key, raises KeyError if there is no such key.
        """
        cdef node_t *node = ct_ceiling_node(self.root, key)
        if node == NULL:  # given key is greater than max-key in tree
            raise KeyError(str(key))
        return <object> node.key, <object> node.value

    def iter_items(self, start_key=None, end_key=None, reverse=False):
        """Iterates over the (key, value) items of the associated tree,
        in ascending order if reverse is True, iterate in descending order,
        reverse defaults to False
        """
        if self._count == 0:
            return
        cdef bint iter_all = (start_key is None) and (end_key is None)
        cdef int direction = 1 if reverse else 0
        cdef int other = 1 - direction
        cdef bint go_down = True
        cdef node_stack_t *st = stack_init(32)
        cdef node_t *node

        node = self.root
        while True:
            if node.link[direction] != NULL and go_down:
                stack_push(st, node)
                node = node.link[direction]
            else:
                if iter_all:
                    yield <object>node.key, <object>node.value
                elif (start_key is None or ct_compare(start_key, <object>node.key) < 1) and \
                     (end_key is None or ct_compare(end_key, <object>node.key) > 0):
                    yield <object>node.key, <object>node.value
                if node.link[other] != NULL:
                    node = node.link[other]
                    go_down = True
                else:
                    if stack_is_empty(st):
                        stack_delete(st)
                        return  # all done
                    node = stack_pop(st)
                    go_down = False

    def pop_item(self):
        """ T.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if T is empty
        """
        if self.count == 0:
            raise KeyError("popitem(): tree is empty")

        cdef node_t *node = get_leaf_node(self.root)
        key = <object> node.key
        value = <object> node.value
        self.remove(key)
        return key, value

    def foreach(self, func, int order=0):
        """ Visit all tree nodes and process key, value.

        parm func: function(key, value)
        param int order: inorder = 0, preorder = -1, postorder = +1
        """
        if self._count == 0:
            return
        cdef node_stack_t *st = stack_init(128)
        cdef node_t *node = self.root
        cdef bint go_down = True

        while True:
            if order == -1:
                func(<object>node.key, <object>node.value)
            if node.link[0] != NULL and go_down:
                stack_push(st, node)
                node = node.link[0]
            else:
                if order == 0:
                    func(<object>node.key, <object>node.value)
                if node.link[1] != NULL:
                    node = node.link[1]
                    go_down = True
                else:
                    if stack_is_empty(st):
                        stack_delete(st)
                        return  # all done
                    node = stack_pop(st)
                    if order == +1:
                        func(<object>node.key, <object>node.value)
                    go_down = False


cdef class _BinaryTree(_BaseTree):
    def insert(self, key, value):
        res = ct_bintree_insert(&self.root, key, value)
        if res < 0:
            raise MemoryError('Can not allocate memory for node structure.')
        self._count += res

    def remove(self, key):
        cdef int result
        result = ct_bintree_remove(&self.root, key)
        if result == 0:
            raise KeyError(str(key))
        else:
            self._count -= 1

class FastBinaryTree(_BinaryTree, _ABCTree):
    pass

cdef class _AVLTree(_BaseTree):
    def insert(self, key, value):
        res = avl_insert(&self.root, key, value)
        if res < 0:
            raise MemoryError('Can not allocate memory for node structure.')
        else:
            self._count += res

    def remove(self, key):
        cdef int result
        result =  avl_remove(&self.root, key)
        if result == 0:
            raise KeyError(str(key))
        else:
            self._count -= 1

class FastAVLTree(_AVLTree, _ABCTree):
    pass

cdef class _RBTree(_BaseTree):
    def insert(self, key, value):
        res = rb_insert(&self.root, key, value)
        if res < 0:
            raise MemoryError('Can not allocate memory for node structure.')
        else:
            self._count += res

    def remove(self, key):
        cdef int result
        result =  rb_remove(&self.root, key)
        if result == 0:
            raise KeyError(str(key))
        else:
            self._count -= 1

class FastRBTree(_RBTree, _ABCTree):
    pass