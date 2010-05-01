#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython red-black-tree module
# Created: 28.04.2010

from itertools import izip

__all__ = ['cRBTree']

cdef class Node:
    cdef Node left
    cdef Node right
    cdef object key
    cdef object value
    cdef bint red

    def __init__(self, object key=None, object value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.red = True

    cdef Node link(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        # this is a little bit faster as __getitem__
        return self.left if key == 0 else self.right

    def __getitem__(self, int key):
        """Get left (key==0) or right (key==1) node by index"""
        return self.left if key == 0 else self.right

    def __setitem__(self, int key, Node value):
        """Set left (key==0) or right (key==1) node by index"""
        if key == 0:
            self.left = value
        else:
            self.right = value

    cdef void free(self):
        self.left = None
        self.right = None
        self.key = None
        self.value = None

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

cdef void tree_to_str(Node node, result):
    if node is not None:
        tree_to_str(node.left, result)
        tree_to_str(node.right, result)
        result.append(repr(node.key)+': '+repr(node.value))

cdef void clear_tree(Node node):
    if node is not None:
        clear_tree(node.left)
        clear_tree(node.right)
        node.free()

cdef void traverse_inorder(Node node, object func):
    if node is not None:
        traverse_inorder(node.left, func)
        func(node.value)
        traverse_inorder(node.right, func)

cdef void traverse_preorder(Node node, object func):
    if node is not None:
        func(node.value)
        traverse_preorder(node.left, func)
        traverse_preorder(node.right, func)

cdef void traverse_postorder(Node node, object func):
    if node is not None:
        traverse_postorder(node.left, func)
        traverse_postorder(node.right, func)
        func(node.value)

cdef void add_values(Node node, result):
    if node is not None:
        add_values(node.left, result)
        result.append(node.value)
        add_values(node.right, result)

cdef void add_keys(Node node, result):
    if node is not None:
        add_keys(node.left, result)
        result.append(node.key)
        add_keys(node.right, result)

cdef Node get_leaf(Node node):
    while True:
        if node.left is not None:
            node = node.left
        elif node.right is not None:
            node = node.right
        else:
            return node

cdef class cRBTree:
    cdef Node root
    cdef object compare
    cdef int _count

    def __init__(self, items=[], compare=None):
        self.root = None
        self.compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    def copy(self):
        return cRBTree(self)

    def __copy__(self):
        return self.copy()

    def __repr__(self):
        result = []
        tree_to_str(self.root, result)
        return "{{{0}}}".format(", ".join(result))

    def has_key(self, key):
        cdef Node node
        node = self.find_node(key)
        return node is not None

    def __contains__(self, key):
        return self.has_key(key)

    def clear(self):
        clear_tree(self.root)
        self._count = 0
        self.root = None

    def __len__(self):
        return self._count

    def is_empty(self):
        return (self.root is None)

    def keys(self):
        result = []
        add_keys(self.root, result)
        return result

    def iterkeys(self):
        return iter(self.keys())

    def __iter__(self):
        return iter(self.keys())

    def values(self):
        result = list()
        add_values(self.root, result)
        return result

    def itervalues(self):
        return iter(self.values())

    def iteritems(self):
        return izip(self.keys(), self.values())

    def items(self):
        return zip(self.keys(), self.values())

    def __getitem__(self, key):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            raise KeyError(unicode(key))
        return node.value

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def setdefault(self, key, default=None):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            self.insert(key, default)
            return default
        return node.value

    def foreach(self, func, order='inorder'):
        """Visit all tree nodes and process node-value.

        func -- function(node.value)

        order -- 'inorder', 'preorder', 'postorder'
        """
        if order=='inorder':
            traverse_inorder(self.root, func)
        elif order=='postorder':
            traverse_postorder(self.root, func)
        elif order=='preorder':
            traverse_preorder(self.root, func)
        else:
            raise ValueError("foreach(): unknown order '{0}'.".format(order))

    def update(self, items):
        try:
            generator = items.iteritems()
        except AttributeError:
            generator = iter(items)

        for key, value in generator:
            self.insert(key, value)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        tree = cls()
        for key in iterable:
            tree.insert(key, value)
        return tree

    def get(self, key, default=None):
        cdef Node node
        node = self.find_node(key)
        if node is None:
            return default
        else:
            return node.value

    def pop(self, key, *args):
        cdef Node node
        if len(args) > 1:
            raise TypeError("pop expected at most 2 arguments, got {0}".format(
                              1+len(args)))

        node = self.find_node(key)
        if node is None:
            if len(args) == 0:
                raise KeyError(unicode(key))
            else:
                return args[0]
        value = node.value
        self.remove(key)
        return value

    def popitem(self):
        cdef Node node
        if self.is_empty():
            raise KeyError("popitem(): tree is empty")
        node = get_leaf(self.root)
        result = (node.key, node.value)
        self.remove(node.key)
        return result

    cdef Node find_node(self, object key):
        cdef int cval
        cdef Node node
        compare = self.compare
        node = self.root
        while True:
            if node is None:
                return None
            cval = <int>compare(key, node.key)
            if cval == 0:
                return node
            elif cval < 0:
                node = node.left
            else:
                node = node.right

    cdef Node new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        cdef Node head, t, grandparent, node, q
        cdef int direction, direction2, last, cmp_res

        compare = self.compare
        if self.root is None: # Empty tree case
            head = self.new_node(key, value)
            head.red = False # make root black
            self.root = head
            return

        head = Node() # False tree root
        grandparent = None # Grandparent
        t = head # parent
        node = None # Iterator
        direction = 0
        last = 0

        # Set up helpers
        t.right = self.root
        q = t.right
        # Search down the tree
        while True:
            if (q is None):# Insert new node at the bottom
                q = self.new_node(key, value)
                node[direction] = q
            elif is_red(q.left) and is_red(q.right):# Color flip
                q.red = True
                q.left.red = False
                q.right.red = False

            # Fix red violation
            if is_red(q) and is_red(node):
                direction2 = 1 if t.right is grandparent else 0
                if q is node.link(last):
                    t[direction2] = jsw_single(grandparent, 1-last)
                else:
                    t[direction2] = jsw_double(grandparent, 1-last)

            # Stop if found
            cmp_res = compare(key, q.key)
            if cmp_res == 0:
                q.value = value #set new value for key
                break

            last = direction
            if cmp_res < 0:
                direction = 0 # key < q.key
            else:
                direction = 1 # key > q.key

            # Update helpers
            if grandparent is not None:
                t = grandparent
            grandparent = node
            node = q
            q = q.link(direction)

        head.red = False # make root black
        self.root = head.right # Update root

    def remove(self, key):
        cdef Node head, node, parent, grandparent, found
        cdef int direction, last, direction2

        if self.root is None:
            raise KeyError(str(key))
        compare = self.compare
        head = Node() # False tree root
        node = head
        node.right = self.root
        parent = None
        grandparent = None
        found = None # Found item
        direction = 1

        # Search and push a red down
        while (node.link(direction) is not None):
            last = direction

            # Update helpers
            grandparent = parent
            parent = node
            node = node.link(direction)
            direction = int(compare(node.key, key) < 0)

            # Save found node
            if compare(node.key, key) == 0:
                found = node

            # Push the red node down
            if (not is_red(node)) and (not is_red(node.link(direction))):
                if is_red(node.link(1-direction)):
                    parent[last] = jsw_single(node, direction)
                    parent = parent.link(last)
                elif not is_red(node.link(1-direction)):
                    s = parent.link(1-last)
                    if s is not None:
                        if (not is_red(s.link(1-last))) and \
                           (not is_red(s.link(last))):
                            # Color flip
                            parent.red = False
                            s.red = True
                            node.red = True
                        else:
                            direction2 = int(grandparent.right == parent)
                            if is_red(s.link(last)):
                                grandparent[direction2] = jsw_double(parent, last)
                            elif is_red(s.link(1-last)):
                                grandparent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            grandparent.link(direction2).red = True
                            node.red = True
                            grandparent[direction2].left.red = False
                            grandparent[direction2].right.red = False

        # Replace and remove if found
        if found is not None:
            found.key = node.key
            found.value = node.value
            parent[int(parent.right == node)] = node[int(node.left == None)]
            node.free()
            self._count -= 1

        # Update root and make it black
        self.root = head.right
        if self.root is not None:
            self.root.red = False
