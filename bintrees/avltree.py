#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: AVL tree module
# Created: 28.04.2010

# Copyright (c) 2005-2008, Simon Howard
#
# Permission to use, copy, modify, and/or distribute this software
# for any purpose with or without fee is hereby granted, provided
# that the above copyright notice and this permission notice appear
# in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from basetree import BaseTree

__all__ = ['AVLTree']

AVL_LEFT = 0
AVL_RIGHT = 1

class TreeNode(object):
    __slots__ = ['left', 'right', 'parent', 'height', 'key', 'value']

    def __init__(self, key=None, value=None, parent=None):
        self.left = None
        self.right = None
        self.parent = parent
        self.key = key
        self.value = value
        self.height = 1

    def __getitem__(self, key):
        """Get left or right node by index"""
        if key == 0:
            return self.left
        elif key == 1:
            return self.right
        else:
            raise KeyError(str(key))

    def __setitem__(self, key, value):
        """Set left or right node by index"""
        if key == 0:
            self.left = value
        elif key == 1:
            self.right = value
        else:
            raise KeyError(str(key))

    def free(self):
        """Remove all references."""
        self.parent = None
        self.left = None
        self.right = None
        self.key = None
        self.value = None

    def update_height(self):
        """Update the "height" variable of a node, from the heights of its
        children.  This does not update the height variable of any parent nodes.
        """
        left_height = _subtree_height(self.left)
        right_height = _subtree_height(self.right)

        if left_height > right_height:
            self.height = left_height + 1
        else:
            self.height = right_height + 1

    def node_parent_side(self):
        """ Find what side a node is relative to its parent """
        if self.parent.left is self:
            return AVL_LEFT
        else:
            return AVL_RIGHT

def _subtree_height(node):
    """Get height for node, works also with None-nodes"""
    if node is None:
        return 0
    else:
        return node.height

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
    def copy(self):
        """Returns a shallow copy of this tree"""
        return AVLTree(self) # has no problem with sorted keys
    __copy__ = copy

    def _node_replace(self, node1, node2):
        """ Replace node1 with node2 at its parent. """
        # Set the node's parent pointer.
        if node2 is not None:
            node2.parent = node1.parent
        # The root node?
        if node1.parent is None:
            self.root = node2
        else:
            side = node1.node_parent_side()
            node1.parent[side] = node2
            node1.parent.update_height()

    def _rotate(self, node, direction):
        """ Rotate a section of the tree.  'node' is the node at the top
         of the section to be rotated.  'direction' is the direction in
         which to rotate the tree: left or right, as shown in the following
         diagram:

             Left rotation:              Right rotation:

                  B                             D
                 / \                           / \
                A   D                         B   E
                   / \                       / \
                  C   E                     A   C

             is rotated to:              is rotated to:

                    D                           B
                   / \                         / \
                  B   E                       A   D
                 / \                             / \
                A   C                           C   E

        """
        # The child of this node will take its place:
        # for a left rotation, it is the right child, and vice versa.
        other_side = 1 - direction
        new_root = node[other_side]

        # Make new_root the root, update parent pointers.
        self._node_replace(node, new_root)

        # Rearrange pointers
        node[other_side] = new_root[direction]
        new_root[direction] = node

        # Update parent references
        node.parent = new_root

        child = node[other_side]
        if child is not None:
            child.parent = node

        # Update heights of the affected nodes
        new_root.update_height()
        node.update_height()
        return new_root


    def _node_balance(self, node):
        """ Balance a particular tree node.
        Returns the root node of the new subtree which is replacing the old one.
        """
        left_subtree = node.left
        right_subtree = node.right
        # Check the heights of the child trees.  If there is an unbalance
        # (difference between left and right > 2), then rotate nodes
        # around to fix it

        diff = _subtree_height(right_subtree) - _subtree_height(left_subtree)
        if diff >= 2:
            # Biased toward the right side too much.
            child = right_subtree

            if _subtree_height(child.right) < _subtree_height(child.left):
                # If the right child is biased toward the left
                # side, it must be rotated right first (double rotation)
                self._rotate(right_subtree, AVL_RIGHT)

                # Perform a left rotation.  After this, the right child will
                # take the place of this node.  Update the node pointer.
                node = self._rotate(node, AVL_LEFT);

        elif diff <= -2:
            # Biased toward the left side too much.
            child = node.left
            if _subtree_height(child.left) < _subtree_height(child.right):
                # If the left child is biased toward the right
                # side, it must be rotated right left (double rotation)
                self._rotate(left_subtree, AVL_LEFT)

            # Perform a right rotation.  After this, the left child will
            # take the place of this node.  Update the node pointer.

            node = self._rotate(node, AVL_RIGHT)
        #Update the height of this node
        node.update_height()
        return node

    def _balance_to_root(self, root):
        """ Walk up the tree from the given node, performing any needed
        rotations
        """
        rover = root
        while rover is not None:
            # Balance this node if necessary
            root = self._node_balance(rover)
            # Go to this node's parent
            rover = root.parent
        self.root = root

    def insert(self, key, value):
        """Insert a key, value pair"""
        # Walk down the tree until we reach a None pointer
        rover = self.root
        previous_node = None
        compare = self.compare

        while rover is not None:
            previous_node = rover
            cmp_res = compare(key, rover.key)
            if cmp_res < 0:
                rover = rover.left
                ipos = AVL_LEFT
            elif cmp_res > 0:
                rover = rover.right
                ipos = AVL_RIGHT
            else: # replace existing value
                rover.value = value
                return

        # Create a new node.  Use the last node visited as the parent link.
        new_node = TreeNode(key, value, previous_node)
        # Keep track of the number of entries
        self._count += 1

        # Insert at the None-pointer that was reached
        if previous_node is not None:
            previous_node[ipos] = new_node

        # Rebalance the tree, starting from the previous node.
        self._balance_to_root(previous_node)

        if self.root is None:
            self.root = new_node

    def _get_replacement(self, node):
        """ Find the nearest node to the given node, to replace it.
        The node returned is unlinked from the tree.
        Returns None if the node has no children.
        """
        left_subtree = node.left
        right_subtree = node.right

        # No children?
        if (left_subtree is None) and (right_subtree is None):
            return None

        # Pick a node from whichever subtree is taller.  This helps to
        # keep the tree balanced.

        left_height = _subtree_height(left_subtree)
        right_height = _subtree_height(right_subtree)

        if left_height < right_height:
            side = AVL_RIGHT
        else:
            side = AVL_LEFT

        # Search down the tree, back towards the center.
        result = node[side]
        other_side = 1 - side
        while (result[other_side] is not None):
            result = result[other_side]

        # Unlink the result node, and hook in its remaining child
        # (if it has one) to replace it.
        child = result[side]
        self._node_replace(result, child)

        # Update the subtree height for the result node's old parent.
        if result.parent is not None:
            result.parent.update_height()
        return result

    def _remove_node(self, node):
        """ Remove a node from a tree """
        # The node to be removed must be swapped with an "adjacent"
        # node, ie. one which has the closest key to this one. Find
        # a node to swap with.

        swap_node = self._get_replacement(node)
        if swap_node is None:
            # This is a leaf node and has no children, therefore
            # it can be immediately removed.
            # Unlink this node from its parent.
            self._node_replace(node, None)

            # Start rebalancing from the parent of the original node
            balance_startpoint = node.parent
        else:
            # We will start rebalancing from the old parent of the
            # swap node.  Sometimes, the old parent is the node we
            # are removing, in which case we must start rebalancing
            # from the swap node.
            if swap_node.parent is None:
                balance_startpoint = swap_node
            else:
                balance_startpoint = swap_node.parent
            # Copy references in the node into the swap node
            for i in (0, 1):
                child = node[i]
                swap_node[i] = child
                if child is not None:
                    child.parent = swap_node
            swap_node.height = node.height

            # Link the parent's reference to this node
            self._node_replace(node, swap_node);

        # Rebalance the tree
        self._balance_to_root(balance_startpoint)
        node.free()
        self._count -= 1

    def remove(self, key):
        """ Remove item by key from tree"""
        # Find the node to remove
        node = self._find_node(key)
        if node is None:
            # Not found in tree
            raise KeyError(str(key))
        # Remove the node
        self._remove_node(node)
