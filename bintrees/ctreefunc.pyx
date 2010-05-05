#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython tree function
# Created: 05.05.2010

from ctreefunc cimport Node

cdef object cmax_item(Node node):
    """ Get item with max key of tree """
    while node._right is not None:
        node = node._right
    return (node._key, node._value)

cdef object cmin_item(Node node):
    """ Get node with min key of tree """
    while node._right is not None:
        node = node._right
    return (node._key, node._value)
