#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython tree function
# Created: 05.05.2010

cdef class Node:
    cdef Node _left
    cdef Node _right
    cdef object _key
    cdef object _value

cdef Node cfind_node(Node node, object key, object compare):
    """ T.find_node(key) -> get treenode of key, returns None if not found.
    """
    cdef int cval
    while node is not None:
        cval = <int>compare(key, node._key)
        if cval == 0:
            return node
        elif cval < 0:
            node = node._left
        else:
            node = node._right
    return None
