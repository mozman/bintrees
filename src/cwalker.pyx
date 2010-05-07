#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: tree walker for cython trees
# Created: 07.05.2010

DEF MAXSTACK=64

cdef extern from "ctrees.h":
    ctypedef struct PyObject:
        pass

    ctypedef struct node_t:
        node_t* link[2]
        PyObject *key
        PyObject *value

cdef class cWalker:
    cdef node_t *node
    cdef node_t *root
    cdef node_t *stack[MAXSTACK]
    cdef int stackptr
    cdef object compare

    def __init__(self, node_t *root, object compare):
        self.root = root
        self.node = root
        self.stackptr = 0

    def reset(self):
        self.stackptr = 0
        self.node = self.root

    @property
    def key(self):
        return <object> self.node.key

    @property
    def value(self):
        return <object> self.node.value

    @property
    def item(self):
        return (<object>self.node.key, <object>self.node.value)

    @property
    def is_valid(self):
        return self.node != NULL

    def goto(self, key):
        cdef int cval
        while self._node is not None:
            cval = <int>self.compare(key, <object> self.node.key)
            if cval == 0:
                return True
            elif cval < 0:
                self.node = self.node.link[0]
            else:
                self.node = self.node.link[1]
        return False

    cpdef push(self):
        self.stack[stackptr] = self.node
        self.stackptr += 1
        if stackptr > MAXSTACK: # raise error, this is a problem for unbalanced trees
            stackptr = MAXSTACK

    cpdef pop(self):
        self.stackptr -= 1
        self.node = <node_t *>self.stack[stackptr]

    def stack_is_empty(self):
        return self.stackptr == 0

    def goto_leaf(self):
        """ get a leaf node """
        while self.node != NULL:
            if self.node.link[0] != NULL:
                self.node = self.node.link[0]
            elif self.node.link[1] != NULL:
                self.node = self.node.link[1]
            else:
                return

    def has_child(self, int direction):
        return self.node.link[direction] != NULL

    def down(self, int direction):
        self.node = self.node.link[direction]

    def go_left(self):
        self.node = self.node.link[0]

    def go_right(self):
        self.node = self.node.link[1]

    def has_left(self):
        return self.node.link[0] != NULL

    def has_right(self):
        return self.node.link[1] != NULL

    def succ_item(self, key):
        """ Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist.
        """
        cdef object succ
        cdef int cval

        self.node = self.root
        self.stackptr = 0
        succ = None
        while self.node != NULL:
            cval = <int> self.compare(key, <object>self.node.key)
            if cval == 0:
                break
            elif cval < 0:
                if (succ is None) or (<int>self.compare(<object>self.node.key, succ[0]) < 0):
                    succ = self.item
                self.node = self.node.link[0]
            else:
                self.node = self.node.link[1]

        if self.node == NULL: # stay at dead end
            raise KeyError(unicode(key))
        # found node of key
        if self.node.link[1] != NULL:
            # find smallest node of right subtree
            self.node = self.node.link[1]
            while self.node.link[0] != NULL:
                self.node = self.node.link[0]
            if succ is None:
                succ = self.item
            elif <int>self.compare(<object> self.node.key, succ[0]) < 0:
                succ = self.item
        elif succ is None: # given key is biggest in tree
            raise KeyError(unicode(key))
        return succ

    def prev_item(self, key):
        """ Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist.
        """
        cdef object prev
        cdef int cval

        self.node = self.root
        self.stackptr = 0
        prev = None
        while self.node != NULL:
            cval = <int>self.compare(key, <object> self.node.key)
            if cval == 0:
                break
            elif cval < 0:
                self.node = self.node.link[0]
            else:
                if (prev is None) or (<int> self.compare(<object> self.node.key, prev[0]) > 0):
                    prev = self.item
                self.node = self.node.link[1]

        if self.node == NULL: # stay at dead end (None)
            raise KeyError(unicode(key))
        # found node of key
        if self.node.link[0] != NULL:
            # find biggest node of left subtree
            self.node = self.node.link[0]
            while self.node.link[1] != NULL:
                self.node = self.node.link[1]
            if prev is None:
                prev = self.item
            elif <int>self.compare(<object>self.node.key, prev[0]) > 0:
                prev = self.item
        elif prev is None: # given key is smallest in tree
            raise KeyError(unicode(key))
        return prev
