#!/usr/bin/env python
#coding:utf-8
# Author:  mozman (python version)
# Purpose: avl tree module (Julienne Walker's unbounded none recursive algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_avl.aspx
# Created: 01.05.2010

# Conclusion of Julienne Walker

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

from treemixin import TreeMixin
from array import array

__all__ = ['AVLTree']

MAXSTACK = 32

class Node(object):
    """ Internal object, represents a treenode """
    __slots__ = ['left', 'right', 'balance', 'key', 'value']
    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.balance = 0

    def __getitem__(self, key):
        """ x.__getitem__(key) <==> x[key], where key is 0 (left) or 1 (right) """
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """ x.__setitem__(key, value) <==> x[key]=value, where key is 0 (left) or 1 (right) """
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
    rlh = height(root.left)
    rrh = height(root.right)
    slh = height(save[other_side])
    root.balance = max(rlh, rrh) + 1
    save.balance = max(slh, root.balance) + 1
    return save

def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)


class AVLTree(TreeMixin):
    """
    AVLTree implements a balanced binary tree with a dict-like interface.

    see: http://en.wikipedia.org/wiki/AVL_tree

    In computer science, an AVL tree is a self-balancing binary search tree, and
    it is the first such data structure to be invented. In an AVL tree, the
    heights of the two child subtrees of any node differ by at most one;
    therefore, it is also said to be height-balanced. Lookup, insertion, and
    deletion all take O(log n) time in both the average and worst cases, where n
    is the number of nodes in the tree prior to the operation. Insertions and
    deletions may require the tree to be rebalanced by one or more tree rotations.

    The AVL tree is named after its two inventors, G.M. Adelson-Velskii and E.M.
    Landis, who published it in their 1962 paper "An algorithm for the
    organization of information."

    AVLTree([compare]) -> new empty tree.
    AVLTree(mapping, [compare]) -> new tree initialized from a mapping
    AVLTree(seq, [compare]) -> new tree initialized from seq

    Methods
    -------

    * __contains__(k) -> True if T has a key k, else False, O(log(n))
    * __delitem__(y) <==> del T[y], O(log(n))
    * __getitem__(y) <==> T[y], O(log(n))
    * __iter__() <==> iter(T)
    * __len__() <==> len(T), O(1)
    * __max__() <==> max(T), get max item (k,v) of T, O(log(n))
    * __min__() <==> min(T), get min item (k,v) of T, O(log(n))
    * __and__(other) <==> T & other, intersection
    * __or__(other) <==> T | other, union
    * __sub__(other) <==> T - other, difference
    * __xor__(other) <==> T ^ other, symmetric_difference
    * __repr__() <==> repr(T)
    * __setitem__(k, v) <==> T[k] = v, O(log(n))
    * clear() -> None, Remove all items from T, , O(n)
    * copy() -> a shallow copy of T, O(n*log(n))
    * discard(k) -> None, remove k from T, if k is present, O(log(n))
    * get(k[,d]) -> T[k] if k in T, else d, O(log(n))
    * has_key(k) -> True if T has a key k, else False, O(log(n))
    * is_empty() -> True if len(T) == 0, O(1)
    * items([reverse]) -> list of T's (k, v) pairs, as 2-tuples, O(n)
    * keys([reverse]) -> list of T's keys, O(n)
    * pop(k[,d]) -> v, remove specified key and return the corresponding value, O(log(n))
    * popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple, O(log(n))
    * setdefault(k[,d]) -> T.get(k, d), also set T[k]=d if k not in T, O(log(n))
    * update(E) -> None.  Update T from dict/iterable E, O(E*log(n))
    * values([reverse]) -> list of T's values, O(n)

    walk forward/backward, O(log(n))

    * prev_item(key) -> get (k, v) pair, where k is predecessor to key, O(log(n))
    * prev_key(key) -> k, get the predecessor of key, O(log(n))
    * succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key, O(log(n))
    * succ_key(key) -> k, get the successor of key, O(log(n))

    traverse tree

    * iteritems([reverse]) -> an iterator over the (k, v) items of T, O(n)
    * iterkeys([reverse]) -> an iterator over the keys of T, O(n)
    * itervalues([reverse]) -> an iterator over the values of T, O(n)
    * treeiter([rtype, reverse]) -> TreeIterator
    * foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node, O(n)

    Heap methods

    * max_item() -> get biggest (key, value) pair of T, O(log(n))
    * max_key() -> get biggest key of T, O(log(n))
    * min_item() -> get smallest (key, value) pair of T, O(log(n))
    * min_key() -> get smallest key of T, O(log(n))
    * pop_min() -> (k, v), remove item with minimum key, O(log(n))
    * pop_max() -> (k, v), remove item with maximum key, O(log(n))
    * nlargest(i[,pop]) -> get list of i largest items (k, v), O(i*log(n))
    * nsmallest(i[,pop]) -> get list of i smallest items (k, v), O(i*log(n))

    Index methods (access by index slow)

    * index(k) -> index of key k, O(n)
    * item_at(i)-> get (k,v) pair as a 2-tuple at index i, i<0 count from end, O(n)
    * T[s:e:i] -> slicing from start s to end e, step i, O(n)
    * del T[s:e:i] -> remove items by slicing, O(n)

    Set methods (using frozenset)

    * intersection(t1, t2, ...) -> Tree with keys *common* to all trees
    * union(t1, t2, ...) -> Tree with keys from *either* trees
    * difference(t1, t2, ...) -> Tree with keys in T but not any of t1, t2, ...
    * symmetric_difference(t1) -> Tree with keys in either T and t1  but not both
    * issubset(S) -> True if every element in T is in S
    * issuperset(S) -> True if every element in S is in T
    * isdisjoint(S) ->  True if T has a null intersection with S

    Classmethods

    * fromkeys(S[,v]) -> New tree with keys from S and values equal to v.
    """
    def __init__(self, items=[], compare=None):
        """ x.__init__(...) initializes x; see x.__class__.__doc__ for signature """
        self._root = None
        self._compare = compare if compare is not None else cmp
        self._count = 0
        self.update(items)

    def clear(self):
        """ T.clear() -> None.  Remove all items from T. """
        def _clear(node):
            if node is not None:
                _clear(node.left)
                _clear(node.right)
                node.free()
        _clear(self._root)
        self._count = 0
        self._root = None

    @property
    def count(self):
        """ count of items """
        return self._count

    @property
    def root(self):
        """ root node of T """
        return self._root

    @property
    def compare(self):
        """ compare function of T """
        return self._compare

    def _new_node(self, key, value):
        """ Create a new treenode """
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        """ T.insert(key, value) <==> T[key] = value, insert key, value into Tree """
        if self._root is None:
            self._root = self._new_node(key, value)
        else:
            node_stack = [] # node stack
            dir_stack = array('I') # direction stack
            done = False
            top = 0
            node = self._root
            # search for an empty link, save path
            while True:
                direction = 1 if self._compare(key, node.key) > 0 else 0
                dir_stack.append(direction)
                node_stack.append(node)
                if node[direction] is None:
                    break
                node = node[direction]

            # Insert a new node at the bottom of the tree
            node[direction] = self._new_node(key, value)

            # Walk back up the search path
            top = len(node_stack) - 1
            while (top >= 0) and not done:
                direction = dir_stack[top]
                other_side = 1 - direction
                topnode = node_stack[top]
                left_height = height(topnode[direction])
                right_height = height(topnode[other_side])

                # Terminate or rebalance as necessary */
                if (left_height-right_height == 0):
                    done = True
                if (left_height-right_height >= 2):
                    a = topnode[direction][direction]
                    b = topnode[direction][other_side]

                    if height(a) >= height(b):
                        node_stack[top] = jsw_single(topnode, other_side)
                    else:
                        node_stack[top] = jsw_double(topnode, other_side)

                    # Fix parent
                    if top != 0:
                        node_stack[top-1][dir_stack[top-1]] = node_stack[top]
                    else:
                        self._root = node_stack[0]
                    done = True

                # Update balance factors
                topnode = node_stack[top]
                left_height = height(topnode[direction])
                right_height = height(topnode[other_side])

                topnode.balance = max(left_height, right_height) + 1
                top -= 1

    def remove(self, key):
        """ T.remove(key) <==> del T[key], remove item <key> from tree """
        if self._root is None:
            raise KeyError(str(key))
        else:
            compare = self._compare
            node_stack = [None] * MAXSTACK # node stack
            dir_stack = array('I', [0] * MAXSTACK) # direction stack
            top = 0
            node = self._root

            while True:
                # Terminate if not found
                if node is None:
                    raise KeyError(str(key))
                elif compare(node.key, key)==0:
                    break

                # Push direction and node onto stack
                direction = 1 if compare(key, node.key) > 0 else 0
                dir_stack[top] = direction

                node_stack[top] = node
                node = node[direction]
                top += 1

            # Remove the node
            if (node.left is None) or (node.right is None):
                # Which child is not null?
                direction = 1 if node.left is None else 0

                # Fix parent
                if top != 0:
                    node_stack[top-1][dir_stack[top-1]] = node[direction]
                else:
                    self._root = node[direction]
                node.free()
                self._count -= 1
            else:
                # Find the inorder successor
                heir = node.right

                # Save the path
                dir_stack[top] = 1
                node_stack[top] = node
                top += 1

                while (heir.left is not None):
                    dir_stack[top] = 0
                    node_stack[top] = heir
                    top += 1
                    heir = heir.left

                # Swap data
                node.key = heir.key
                node.value = heir.value

                # Unlink successor and fix parent
                xdir = 1 if compare(node_stack[top-1], node) == 0 else 0
                node_stack[top-1][xdir] = heir.right
                heir.free()
                self._count -= 1

            # Walk back up the search path
            top -= 1
            while top >= 0:
                direction = dir_stack[top]
                other_side = 1 - direction
                topnode = node_stack[top]
                left_height = height(topnode[direction])
                right_height = height(topnode[other_side])
                b_max = max(left_height, right_height)

                # Update balance factors
                topnode.balance = b_max + 1

                # Terminate or rebalance as necessary
                if (left_height - right_height) == -1:
                    break
                if (left_height - right_height) <= -2:
                    a = topnode[other_side][direction]
                    b = topnode[other_side][other_side]
                    if height(a) <= height(b):
                        node_stack[top] = jsw_single(topnode, direction)
                    else:
                        node_stack[top] = jsw_double(topnode, direction)
                    # Fix parent
                    if top != 0:
                        node_stack[top-1][dir_stack[top-1]] = node_stack[top]
                    else:
                        self._root = node_stack[0]
                top -= 1
