#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython red-black-tree module
# Created: 28.04.2010

__all__ = ['cRBTree']

cdef class Node:
    cdef Node _left
    cdef Node _right
    cdef object _key
    cdef object _value
    cdef bint red

    def __init__(self, object key=None, object value=None):
        self._left = None
        self._right = None
        self._key = key
        self._value = value
        self.red = True

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

cdef bint is_red(Node node):
    if (node is not None) and node.red:
        return True
    else:
        return False

cdef Node jsw_single(Node root, int direction):
    cdef int other_side
    cdef Node save

    other_side = 1 - direction
    save = root.link(other_side)
    root[other_side] = save.link(direction)
    save[direction] = root
    root.red = True
    save.red = False
    return save

cdef Node jsw_double(Node root, int direction):
    cdef int otherside
    other_side = 1 - direction
    root[other_side] = jsw_single(root.link(other_side), other_side)
    return jsw_single(root, direction)

cdef void clear_tree(Node node):
    if node is not None:
        clear_tree(node._left)
        clear_tree(node._right)
        node.free()


cdef class cRBTree:
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

    cdef Node new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def copy(self):
        return cRBTree(self)

    def __copy__(self):
        return self.copy()

    def clear(self):
        clear_tree(self._root)
        self._count = 0
        self._root = None

    def find_node(self, key):
        cdef int cval
        cdef Node node
        compare = self._compare
        node = self._root
        while True:
            if node is None:
                return None
            cval = <int>compare(key, node._key)
            if cval == 0:
                return node
            elif cval < 0:
                node = node._left
            else:
                node = node._right

    def insert(self, key, value):
        cdef Node head, grand_grand_parent, grand_parent, parent, node
        cdef int direction, direction2, last, cmp_res

        compare = self._compare
        if self._root is None: # Empty tree case
            self._root = self.new_node(key, value)
            self._root.red = False # make root black
            return

        head = Node() # False tree root
        grand_parent = None # Grandparent
        grand_grand_parent = head # parent
        parent = None # Iterator
        direction = 0
        last = 0

        # Set up helpers
        grand_grand_parent._right = self._root
        node = grand_grand_parent._right
        # Search down the tree
        while True:
            if node is None: # Insert new node at the bottom
                node = self.new_node(key, value)
                parent[direction] = node
            elif is_red(node._left) and is_red(node._right):# Color flip
                node.red = True
                node._left.red = False
                node._right.red = False

            # Fix red violation
            if is_red(node) and is_red(parent):
                direction2 = 1 if grand_grand_parent._right is grand_parent else 0
                if node is parent.link(last):
                    grand_grand_parent[direction2] = jsw_single(grand_parent, 1-last)
                else:
                    grand_grand_parent[direction2] = jsw_double(grand_parent, 1-last)

            # Stop if found
            cmp_res = compare(key, node._key)
            if cmp_res == 0:
                node._value = value #set new value for key
                break

            last = direction
            direction = 0 if cmp_res < 0 else 1
            # Update helpers
            if grand_parent is not None:
                grand_grand_parent = grand_parent
            grand_parent = parent
            parent = node
            node = node.link(direction)

        self._root = head._right # Update root
        self._root.red = False # make root black

    def remove(self, key):
        cdef Node head, node, parent, grand_parent, found, sibling
        cdef int direction, last, direction2, cmp_res

        if self._root is None:
            raise KeyError(str(key))
        compare = self._compare
        head = Node() # False tree root
        node = head
        node._right = self._root
        parent = None
        grand_parent = None
        found = None # Found item
        direction = 1

        # Search and push a red down
        while (node.link(direction) is not None):
            last = direction

            # Update helpers
            grand_parent = parent
            parent = node
            node = node.link(direction)
            cmp_res = compare(key, node._key)
            direction = 1 if cmp_res > 0 else 0

            # Save found node
            if cmp_res == 0:
                found = node

            # Push the red node down
            if (not is_red(node)) and (not is_red(node.link(direction))):
                if is_red(node.link(1-direction)):
                    parent[last] = jsw_single(node, direction)
                    parent = parent.link(last)
                elif not is_red(node.link(1-direction)):
                    sibling = parent.link(1-last)
                    if sibling is not None:
                        if (not is_red(sibling.link(1-last))) and \
                           (not is_red(sibling.link(last))):
                            # Color flip
                            parent.red = False
                            sibling.red = True
                            node.red = True
                        else:
                            direction2 = 1 if grand_parent._right is parent else 0
                            if is_red(sibling.link(last)):
                                grand_parent[direction2] = jsw_double(parent, last)
                            elif is_red(sibling.link(1-last)):
                                grand_parent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            grand_parent.link(direction2).red = True
                            node.red = True
                            grand_parent.link(direction2)._left.red = False
                            grand_parent.link(direction2)._right.red = False

        # Replace and remove if found
        if found is not None:
            found._key = node._key
            found._value = node._value
            direction = 1 if parent._right is node else 0
            direction2 = 1 if node._left is None else 0
            parent[direction] = node.link(direction2)
            node.free()
            self._count -= 1

        # Update root and make it black
        self._root = head._right
        if self._root is not None:
            self._root.red = False
