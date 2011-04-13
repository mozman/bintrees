#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: DEPRICATED FastAVLTree
# Created: 28.04.2010
# Copyright (C) 2010, 2011 by Manfred Moitzi
# License: GPLv3
# no longer maintained

__all__ = ['cAVLTree']

DEF MAXSTACK = 32

cdef class Node:
    cdef Node _left
    cdef Node _right
    cdef object _key
    cdef object _value
    cdef int balance

    def __init__(self, key=None, value=None):
        self._left = None
        self._right = None
        self._key = key
        self._value = value
        self.balance = 0

    @property
    def key(self):
        return self._key
    @property
    def value(self):
        return self._value
    @property
    def left(self):
        return self._left
    @property
    def right(self):
        return self._right

    cdef Node link(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        # this is a little bit faster as __getitem__
        return self._left if key == 0 else self._right

    def __getitem__(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        return self._left if key == 0 else self._right

    def __setitem__(self, int key, Node value):
        """Set left (key==0) or right (key==1) node by index"""
        if key == 0:
            self._left = value
        else:
            self._right = value

    def free(self):
        self._left = None
        self._right = None
        self._key = None
        self._value = None

cdef void clear_tree(Node node):
    if node is not None:
        clear_tree(node.left)
        clear_tree(node.right)
        node.free()

cdef inline int imax(int a, int b):
    return a if a > b else b

cdef int height(Node node):
    return node.balance if node is not None else -1

cdef Node jsw_single(Node root, int direction):
    cdef Node save
    cdef int other_side
    cdef int rlh, rrh, slh

    other_side = 1 - direction
    save = root.link(other_side)
    root[other_side] = save.link(direction)
    save[direction] = root
    rlh = height(root._left)
    rrh = height(root._right)
    slh = height(save.link(other_side))
    root.balance = imax(rlh, rrh) + 1
    save.balance = imax(slh, root.balance) + 1
    return save

cdef Node jsw_double(Node root, int direction):
    cdef int other_side
    other_side = 1 - direction
    root[other_side] = jsw_single(root.link(other_side), other_side)
    return jsw_single(root, direction)

cdef class cAVLTree:
    cdef Node _root
    cdef object _compare
    cdef int _count

    def __init__(self, items=[], compare=None):
        self._root = None
        self._compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    @property
    def root(self):
        return self._root

    @property
    def compare(self):
        return self._compare

    @property
    def count(self):
        return self._count

    def clear(self):
        clear_tree(self._root)
        self._count = 0
        self._root = None

    cdef Node new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def get_value(self, key):
        cdef int cval
        cdef Node node
        node = self._root
        while node is not None:
            cval = <int>self._compare(key, node._key)
            if cval == 0:
                return node._value
            elif cval < 0:
                node = node._left
            else:
                node = node._right
        raise KeyError(str(key))

    def insert(self, key, value):
        cdef int dir_stack[MAXSTACK]
        cdef Node node, a, b
        cdef int top, direction, other_side
        cdef int left_height, right_height, cmp_res
        cdef bint done

        if self._root is None:
            self._root = self.new_node(key, value)
        else:
            node_stack = [] # node stack
            done = False
            top = 0
            node = self._root
            # search for an empty link, save path
            while True:
                cmp_res = <int>self._compare(key, node._key)
                if cmp_res == 0: # update existing item
                    node._value = value
                    return
                direction = 1 if  cmp_res > 0 else 0
                dir_stack[top] = direction
                node_stack.append(node)
                if node.link(direction) is None:
                    break
                node = node.link(direction)
                top += 1

            # Insert a new node at the bottom of the tree
            node[direction] = self.new_node(key, value)

            # Walk back up the search path
            top -= 1
            while (top >= 0) and not done:
                direction = dir_stack[top]
                other_side = 1 - direction
                node = <Node> node_stack[top]
                left_height = height(node.link(direction))
                right_height = height(node.link(other_side))

                # Terminate or rebalance as necessary */
                if (left_height-right_height == 0):
                    done = True
                if (left_height-right_height >= 2):
                    node = <Node> node_stack[top]
                    a = node.link(direction).link(direction)
                    b = node.link(direction).link(other_side)

                    if height(a) >= height(b):
                        node_stack[top] = jsw_single(node, other_side)
                    else:
                        node_stack[top] = jsw_double(node, other_side)

                    # Fix parent
                    if top != 0:
                        node = <Node> node_stack[top-1]
                        node[dir_stack[top-1]] = node_stack[top]
                    else:
                        self._root = node_stack[0]
                    done = True

                # Update balance factors
                node = <Node> node_stack[top]
                left_height = height(node.link(direction))
                right_height = height(node.link(other_side))

                node.balance = imax(left_height, right_height) + 1
                top -= 1

    def remove(self, key):
        cdef int dir_stack[MAXSTACK]
        cdef Node node, tmp, heir, a, b
        cdef int top, direction, xdir, b_max, other_side
        cdef int left_height, right_height
        cdef bint done

        if self._root is None:
            raise KeyError(str(key))
        else:
            compare = self._compare
            node_stack = [None] * MAXSTACK # node stack
            top = 0
            node = self._root

            while True:
                # Terminate if not found
                if node is None:
                    raise KeyError(str(key))
                elif compare(node._key, key)==0:
                    break

                # Push direction and node onto stack
                direction = 1 if compare(key, node._key) > 0 else 0
                dir_stack[top] = direction

                node_stack[top] = node
                node = node.link(direction)
                top += 1

            # Remove the node
            if (node._left is None) or (node._right is None):
                # Which child is not null?
                direction = 1 if node._left is None else 0

                # Fix parent
                if top != 0:
                    tmp = <Node> node_stack[top-1]
                    tmp[dir_stack[top-1]] = node.link(direction)
                else:
                    self._root = node.link(direction)
                node.free()
                self._count -= 1
            else:
                # Find the inorder successor
                heir = node._right

                # Save the path
                dir_stack[top] = 1
                node_stack[top] = node
                top += 1

                while (heir._left is not None):
                    dir_stack[top] = 0
                    node_stack[top] = heir
                    top += 1
                    heir = heir._left

                # Swap data
                node._key = heir._key
                node._value = heir._value

                # Unlink successor and fix parent
                xdir = 1 if compare(node_stack[top-1], node) == 0 else 0
                node_stack[top-1][xdir] = heir._right
                heir.free()
                self._count -= 1

            # Walk back up the search path
            top -= 1
            while top >= 0:
                direction = dir_stack[top]
                other_side = 1 - direction
                node = <Node> node_stack[top]
                left_height = height(node.link(direction))
                right_height = height(node.link(other_side))
                b_max = imax(left_height, right_height)

                # Update balance factors
                node.balance = b_max + 1

                # Terminate or rebalance as necessary
                if (left_height - right_height) == -1:
                    break
                if (left_height - right_height) <= -2:
                    a = node.link(other_side).link(direction)
                    b = node.link(other_side).link(other_side)
                    if height(a) <= height(b):
                        node_stack[top] = jsw_single(node, direction)
                    else:
                        node_stack[top] = jsw_double(node, direction)
                    # Fix parent
                    if top != 0:
                        node_stack[top-1][dir_stack[top-1]] = node_stack[top]
                    else:
                        self._root = node_stack[0]
                top -= 1

    def prev_item(self, key):
        """ Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist.
        """
        cdef Node node, prev
        cdef int cval

        node = self._root
        if node is None:
            raise KeyError("Tree is empty")
        prev = None
        while node is not None:
            cval = <int>self._compare(key, node._key)
            if cval == 0:
                break
            elif cval < 0:
                node = node._left
            else:
                if (prev is None) or (<int>self._compare(node._key, prev._key) > 0):
                    prev = node
                node = node._right

        if node is None:
            raise KeyError(unicode(key))
        # found node of key
        if node._left is not None:
            # find biggest node of left subtree
            node = node._left
            while node._right is not None:
                node = node._right
            if prev is None:
                prev = node
            elif <int>self._compare(node._key, prev._key) > 0:
                prev = node
        elif prev is None: # given key is smallest in tree
            raise KeyError(unicode(key))
        return (prev._key, prev._value)

    def succ_item(self, key):
        """ Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist.
        """
        cdef Node node, succ
        cdef int cval

        node = self._root
        if node is None:
            raise KeyError("Tree is empty")
        succ = None
        while node is not None:
            cval = <int>self._compare(key, node._key)
            if cval == 0:
                break
            elif cval < 0:
                if (succ is None) or (<int>self._compare(node._key, succ._key) < 0):
                    succ = node
                node = node._left
            else:
                node = node._right

        if node is None:
            raise KeyError(unicode(key))
        # found node of key
        if node._right is not None:
            # find smallest node of right subtree
            node = node._right
            while node._left is not None:
                node = node._left
            if succ is None:
                succ = node
            elif <int>self._compare(node._key, succ._key) < 0:
                succ = node
        elif succ is None: # given key is biggest in tree
            raise KeyError(unicode(key))
        return (succ._key, succ._value)

    def max_item(self):
        """ Get item with max key of tree, raises ValueError if tree is empty. """
        cdef Node node
        node = self._root
        if node is None: # root is None
            raise ValueError("Tree is empty")
        while node._right is not None:
            node = node._right
        return (node._key, node._value)

    def min_item(self):
        """ Get item with min key of tree, raises ValueError if tree is empty. """
        cdef Node node
        node = self._root
        if node is None: # root is None
            raise ValueError("Tree is empty")
        while node._left is not None:
            node = node._left
        return (node._key, node._value)

    def index(self, key):
        """ T.index(k) -> index, raises KeyError if k not in T """
        cdef Node node
        cdef int index
        cdef bint go_down

        node = self._root
        index = 0
        go_down = True
        stack = list()
        while True:
            if node._left is not None and go_down:
                stack.append(node)
                node = node._left
            else:
                if <int>self._compare(node._key, key) == 0:
                    return index
                index += 1
                if node._right is not None:
                    node = node._right
                    go_down = True
                else:
                    if not len(stack):
                        raise KeyError(str(key))
                    node = stack.pop()
                    go_down = False

    def item_at(self, int index):
        """ T.item_at(index) -> item (k,v) """
        cdef Node node
        cdef int counter
        cdef bint go_down

        if index < 0:
            index = self._count + index
        if (index < 0) or (index >= self._count):
            raise IndexError('item_at()')
        node = self._root
        counter = 0
        go_down = True
        stack = list()
        while True:
            if node._left is not None and go_down:
                stack.append(node)
                node = node._left
            else:
                if counter == index:
                    return (node._key, node._value)
                counter += 1
                if node._right is not None:
                    node = node._right
                    go_down = True
                else:
                    if not len(stack):
                        return # all done
                    node = stack.pop()
                    go_down = False
