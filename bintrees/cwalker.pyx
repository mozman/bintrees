#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: tree walker for Cython trees
# Created: 07.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

DEF MAXSTACK=32

from stack cimport *
from ctrees cimport *

cdef class cWalker:
    def __cinit__(self):
        self.root = NULL
        self.node = NULL
        self.stack = stack_init(MAXSTACK)

    def __dealloc__(self):
        stack_delete(self.stack)

    cdef void set_tree(self, node_t *root):
        self.root = root
        self.reset()

    cpdef reset(self):
        stack_reset(self.stack)
        self.node = self.root

    @property
    def key(self):
        return <object> self.node.key

    @property
    def value(self):
        return <object> self.node.value

    @property
    def item(self):
        return <object>self.node.key, <object>self.node.value

    @property
    def is_valid(self):
        return self.node != NULL

    def goto(self, key):
        cdef int cval
        self.node = self.root
        while self.node != NULL:
            cval = ct_compare(key, <object> self.node.key)
            if cval == 0:
                return True
            elif cval < 0:
                self.node = self.node.link[0]
            else:
                self.node = self.node.link[1]
        return False

    cpdef push(self):
        stack_push(self.stack, self.node)

    cpdef pop(self):
        if stack_is_empty(self.stack) != 0:
            raise IndexError('pop(): stack is empty')
        self.node = stack_pop(self.stack)

    cpdef stack_is_empty(self):
        return <bint> stack_is_empty(self.stack)

    cpdef has_child(self, int direction):
        return self.node.link[direction] != NULL

    cpdef down(self, int direction):
        self.node = self.node.link[direction]

    def go_left(self):
        self.node = self.node.link[0]

    def go_right(self):
        self.node = self.node.link[1]

    def has_left(self):
        return self.node.link[0] != NULL

    def has_right(self):
        return self.node.link[1] != NULL