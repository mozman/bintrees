#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: avl tree module (Julienne Walker Recursive Algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_avl.aspx
# unbounded recursive algorithm
# Created: 01.05.2010

# Conclusion of Julian Walker

# AVL trees are about as close to optimal as balanced binary search trees can
# get without eating up resources. You can rest assured that the O(log N)
# performance of binary search trees is guaranteed with AVL trees, but the extra
# bookkeeping required to maintain an AVL tree can be prohibitive, especially
# if deletions are common. Insertion into an AVL tree only requires one single
# or double rotation, but deletion could perform up to O(log N) rotations, as
# in the example of a worst case AVL (ie. Fibonacci) tree. However, those cases
# are rare, and still very fast.

# AVL trees are best used when degenerate sequences are common, and there is
# little or no locality of reference in nodes. That basically means that
# searches are fairly random. If degenerate sequences are not common, but still
# possible, and searches are random then a less rigid balanced tree such as red
# black trees or Andersson trees are a better solution. If there is a significant
# amount of locality to searches, such as a small cluster of commonly searched
# items, a splay tree is theoretically better than all of the balanced trees
# because of its move-to-front design.

from basetree import BaseTree

__all__ = ['AVLTree']

AVL_LEFT = 0
AVL_RIGHT = 1

class Node(object):
    __slots__ = ['left', 'right', 'balance', 'key', 'value']

    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.balance = 0

    def __getitem__(self, key):
        """Get left (==0) or right (==1) node by index"""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """Set left (==0) or right (==1) node by index"""
        if key == 0:
            self.left = value
        else:
            self.right = value

    def free(self):
        """Remove all references."""
        self.left = None
        self.right = None
        self.key = None
        self.value = None

def height(node):
    return node.balance if node is not None else -1

def jsw_single(root, direction):
    other_side = 1 - direction
    save = root[other_side]
    root[other_side] = save[direction]
    save[direction] = root
    rlh = height(root[0])
    rrh = height(root[1])
    slh = height(save[other_side])
    root.balance = max(rlh, rrh) + 1
    save.balance = max(slh, root.balance) +1
    return save

def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)


class AVLTree(BaseTree):
    """AVL Tree (balanced binary search tree)

    The AVL tree structure is a balanced binary tree which stores a collection of
    nodes.  Each node has a key and a value associated with it.  The nodes are
    sorted within the tree based on the order of their keys. Modifications to the
    tree are constructed such that the tree remains balanced at all times (there are
    always roughly equal numbers of nodes on either side of the tree).

    Balanced binary trees have several uses.  They can be used as a mapping
    (searching for a value based on its key), or as a set of keys which is always
    ordered.
    """
    def __init__(self, items=[], compare=None):
        BaseTree.__init__(self, items, compare)
        self._done = True

    def copy(self):
        """Returns a shallow copy of this tree"""
        return AVLTree(self) # has no problem with sorted keys
    __copy__ = copy

    def new_node(self, key, value):
        self._count += 1
        return Node(key, value)

    def _insert_r(self, root, key, value):
        if root is None:
            root = self.new_node(key, value)
        else:
            cmp_res = self.compare(key, root.key)
            direction = 0 if cmp_res < 0 else 1
            if cmp_res == 0:
                root.value = value # replace existing values
                self._done = True
            else:
                root[direction] = self._insert_r(root[direction], key, value)

            if not self._done:
                # Rebalance if necessary
                lh = height(root[direction])
                rh = height(root[1-direction])

                if (lh - rh >= 2):
                    a = root[direction][direction]
                    b = root[direction][1-direction]

                    if (height(a) >= height(b)):
                        root = jsw_single(root, 1-direction)
                    else:
                        root = jsw_double(root, 1-direction)
                    self._done = True

                # Update balance factors
                lh = height(root[direction])
                rh = height(root[1-direction])
                h_max = max(lh, rh)
                root.balance = h_max + 1
        return root

    def insert(self, key, value):
        self._done = False
        self.root = self._insert_r(self.root, key, value)

    def _remove_r (self, root, key):
        if root is not None:
            # Remove node
            cmp_res = self.compare(root.key, key)
            if cmp_res == 0:
                #  Unlink and fix parent
                if (root[0] is None) or  (root[1] is None):
                    direction = 1 if root[0] is None else 0
                    save = root[direction]
                    root.free()
                    self._count -= 1
                    return save
                else:
                    # Find inorder predecessor
                    heir = root[0]
                    while(heir[1] is not None):
                        heir = heir[1]

                    # Copy and set new search data
                    root.key = heir.key
                    root.value = heir.value
                    key = heir.key
            cmp_res = self.compare(root.key, key)
            direction = 1 if cmp_res < 0 else 0
            root[direction] = self._remove_r(root[direction], key)

            if not self._done:
                # Update balance factors
                lh = height(root[direction])
                rh = height(root[1-direction])
                h_max = max(lh, rh)

                root.balance = h_max + 1

                # Terminate or rebalance as necessary
                if (lh-rh == -1):
                    self._done = True
                if (lh-rh <= -2):
                    a = root[1-direction][direction]
                    b = root[1-direction][1-direction]

                    if height(a) <= height(b):
                        root = jsw_single(root, direction)
                    else:
                        root = jsw_double(root, direction)
        return root

    def remove(self, key):
        self._done = False
        self.root = self._remove_r( self.root, key)
