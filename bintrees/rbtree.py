#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: red-black tree module (Julienne Walker Top-Down Algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx
# Created: 01.05.2010

# Conclusion of Julian Walker

# Red black trees are interesting beasts. They're believed to be simpler than
# AVL trees (their direct competitor), and at first glance this seems to be the
# case because insertion is a breeze. However, when one begins to play with the
# deletion algorithm, red black trees become very tricky. However, the
# counterweight to this added complexity is that both insertion and deletion
# can be implemented using a single pass, top-down algorithm. Such is not the
# case with AVL trees, where only the insertion algorithm can be written top-down.
# Deletion from an AVL tree requires a bottom-up algorithm.

# So when do you use a red black tree? That's really your decision, but I've
# found that red black trees are best suited to largely random data that has
# occasional degenerate runs, and searches have no locality of reference. This
# takes full advantage of the minimal work that red black trees perform to
# maintain balance compared to AVL trees and still allows for speedy searches.

# Red black trees are popular, as most data structures with a whimsical name.
# For example, in Java and C++, the library map structures are typically
# implemented with a red black tree. Red black trees are also comparable in
# speed to AVL trees. While the balance is not quite as good, the work it takes
# to maintain balance is usually better in a red black tree. There are a few
# misconceptions floating around, but for the most part the hype about red black
# trees is accurate.

from basetree import BaseTree

__all__ = ['RBTree']

class Node(object):
    __slots__ = ['key', 'value', 'red', 'left', 'right']
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.red = True
        self.left = None
        self.right = None

    def free(self):
        self.left = None
        self.right = None
        self.key = None
        self.value = None

    def __getitem__(self, key):
        """Get left (==0) or right (==1) node by index"""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """Set left (==0) or right (==1) node by index"""
        if key == 0:
            self.left = value
        else:
            self.right = value

def is_red(node):
    if (node is not None) and node.red:
        return True
    else:
        return False

def jsw_single (root, direction):
    other_side = 1 - direction
    save = root[other_side]
    root[other_side] = save[direction]
    save[direction] = root
    root.red = True
    save.red = False
    return save

def jsw_double (root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)

class RBTree(BaseTree):
    def copy(self):
        return RBTree(self) # has no problem with sorted keys
    __copy__ = copy

    def new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        compare = self.compare
        if self.root is None: # Empty tree case
            self.root = self.new_node(key, value)
            self.root.red = False # make root black
            return

        head = Node() # False tree root
        grandparent = None # Grandparent
        t = head # parent
        p = None # Iterator
        direction = 0
        last = 0

        # Set up helpers
        t[1] = self.root
        q = t[1]
        # Search down the tree
        while True:
            if (q is None):# Insert new node at the bottom
                q = self.new_node(key, value)
                p[direction] = q
            elif is_red(q[0]) and is_red(q[1]):# Color flip
                q.red = True
                q[0].red = False
                q[1].red = False

            # Fix red violation
            if is_red(q) and is_red(p):
                direction2 = int(t[1] is grandparent)
                if q is p[last]:
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
            grandparent = p
            p = q
            q = q[direction]

        self.root = head[1] # Update root
        self.root.red = False # make root black

    def remove(self, key):
        compare = self.compare
        if self.root is None:
            return
        head = Node() # False tree root
        node = head
        node.right = self.root
        parent = None
        grandparent = None
        found = None # Found item
        direction = 1

        # Search and push a red down
        while (node[direction] is not None):
            last = direction

            # Update helpers
            grandparent = parent
            parent = node
            node = node[direction]
            direction = int(compare(node.key, key) < 0)

            # Save found node
            if compare(node.key, key) == 0:
                found = node

            # Push the red node down
            if (not is_red(node)) and (not is_red(node[direction])):
                if is_red(node[1-direction]):
                    parent[last] = jsw_single(node, direction)
                    parent = parent[last]
                elif not is_red(node[1-direction]):
                    s = parent[1-last]
                    if s is not None:
                        if (not is_red(s[1-last])) and (not is_red(s[last])):
                            # Color flip
                            parent.red = False
                            s.red = True
                            node.red = True
                        else:
                            direction2 = int(grandparent.right == parent)
                            if is_red(s[last]):
                                grandparent[direction2] = jsw_double(parent, last)
                            elif is_red(s[1-last]):
                                grandparent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            node.red = grandparent[direction2].red = True
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
