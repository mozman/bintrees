#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: red-black tree module
# Created: 28.04.2010

from basetree import BaseTree

__all__ = ['RBTree']

_BLACK = 0
_RED = 1

class TreeNode(object):
    __slots__ = ['key', 'value', 'parent', 'color', 'left', 'right']
    def __init__(self, key, value, parent, color):
        self.key = key
        self.value = value
        self.parent = parent
        self.color = color
        self.left = None
        self.right = None

    def free(self):
        self.left = None
        self.right = None
        self.parent = None
        self.key = None
        self.value = None

    @property
    def grandparent(self):
        if self.parent is not None:
            return self.parent.parent
        else:
            return None

    @property
    def uncle(self):
        try:
            uncle = self.grandparent.left
        except AttributeError:
            return None
        if self.parent is uncle:
            uncle = self.grandparent.right
        return uncle

    @property
    def is_leftnode(self):
        return self is self.parent.left

    @property
    def is_rightnode(self):
        return self is self.parent.right

    @property
    def sibling(self):
        _sibiling = self.parent.left
        if self is _sibiling:
            _sibiling = self.parent.right
        return _sibiling

class RBTree(BaseTree):
    def copy(self):
        return RBTree(self) # has no problem with sorted keys
    __copy__ = copy

    def new_node(self, key, value, parent, color):
        self._count += 1
        return TreeNode(key, value, parent, color)

    def insert(self, key, value):
        if (self.root is None):
            self.root = self.new_node(key, value, None, _BLACK)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        cval = self.compare(key, node.key)
        if cval == 0:
            node.value = value
        elif cval < 0:
            if node.left is None:
                node.left = self.new_node(key, value, node, _RED)
                self._balance_after_insert(node.left)
            else:
                self._insert(node.left, key, value)
        else:
            if node.right is None:
                node.right = self.new_node(key, value, node, _RED)
                self._balance_after_insert(node.right)
            else:
                self._insert(node.right, key, value)

    def _balance_after_insert(self, insertnode):
        def case1(node):
            if node.parent is None:
                node.color = _BLACK
            else:
                case2(node)

        def case2(node):
            if node.parent.color == _RED:
                case3(node)

        def case3(node):
            if (node.uncle is not None) and (node.uncle.color == _RED):
                node.parent.color = _BLACK
                node.uncle.color = _BLACK
                node.grandparent.color = _RED
                case1(node.grandparent)
            else:
                case4(node)

        def case4(node):
            if node.is_rightnode and node.parent.is_leftnode:
                self._rotate_left(node.parent)
                node = node.left
            elif node.is_leftnode and node.parent.is_rightnode:
                self._rotate_right(node.parent)
                node = node.right
            case5(node)

        def case5(node):
            node.parent.color = _BLACK
            node.grandparent.color = _RED
            if node.is_leftnode and node.parent.is_leftnode:
                self._rotate_right(node.grandparent)
            else:
                self._rotate_left(node.grandparent)

        case1(insertnode)

    def _rotate_right(self, w):
    #         W                                  S
    #        / \        _rotate_right(w)        / \
    #       /   \           -------->          /   \
    #      S     Y                            G     W
    #     / \                                      / \
    #    /   \                                    /   \
    #   G     U                                  U     Y

        root = w.parent
        s = w.left
        u = s.right

        if root is not None:
            if w.is_leftnode:
                root.left = s
            else:
                root.right = s
        else:
            self.root = s

        s.right = w
        w.left = u
        if u is not None:
            u.parent = w
        w.parent = s
        s.parent = root

    def _rotate_left(self, s):
    #         W                                  S
    #        / \                                / \
    #       /   \                              /   \
    #      S     Y                            G     W
    #     / \               <--------              / \
    #    /   \          _rotate_left(s)           /   \
    #   G     U                                  U     Y

        root = s.parent
        w = s.right
        u = w.left

        if root is not None:
            if s.is_leftnode:
                root.left = w
            else:
                root.right = w
        else:
            self.root = w

        s.right = u
        w.left = s
        if u is not None:
            u.parent = s
        s.parent = w
        w.parent = root

    def remove(self, key):
        node = self._find_node(key)
        if node is None:
            raise KeyError(unicode(key))
        else:
            if node.left is None:
                child = node.right
            elif node.right is None:
                child = node.left
            else: #left and right not nil
                child = self._smallest_node(node.right)
            self._replace(node, child)
            if (node.color == _BLACK) and (child is not None):
                if child.color == _RED:
                    child.color == _BLACK
                else:
                    self._balance_after_delete(child)
        node.free()

    def _balance_after_delete(self, startnode):
        def case1(node):
            if (node.parent is not None):
                case2(node)

        def case2(node):
            if (node.sibling.color == _RED):
                node.parent.color = _RED
                node.sibling.color = _BLACK
                if node.is_leftnode:
                    self._rotate_left(node.parent)
                else:
                    self._rotate_right(node.parent)
            case3(node)

        def case3(node):
            if (node.parent.color == _BLACK) and \
               (node.sibling.color == _BLACK) and \
               (node.sibling.left.color == _BLACK) and \
               (node.sibling.right.color == _BLACK):
                node.sibling.color = _RED
                case1(node.parent)
            else:
                case4(node)

        def case4(node):
            if (node.parent.color == _RED) and \
               (node.sibling.color == _BLACK) and \
               (node.sibling.left.color == _BLACK) and \
               (node.sibling.right.color == _BLACK):
                node.sibling.color = _RED
                node.parent.color = _BLACK
            else:
                case5(node)

        def case5(node):
            if node.is_leftnode and \
               (node.sibling.color == _BLACK) and \
               (node.sibling.left.color == _RED) and \
               (node.sibling.right.color == _BLACK):

                node.sibling.color = _RED
                node.sibling.left.color = _BLACK
                self._rotate_right(node.sibling)
            elif node.is_rightnode and \
              (node.sibling.color == _BLACK) and \
              (node.sibling.right.color == _RED) and \
              (node.sibling.left.color == _BLACK):
                node.sibling.color = _RED
                node.sibling.right.color = _BLACK
                self._rotate_left(node.sibling)
            case6(node)

        def case6(node):
            node.sibling.color = node.parent.color
            node.parent.color = _BLACK
            if node.is_leftnode:
                node.sibling.right.color = _BLACK
                self._rotate_left(node.parent)
            else:
                node.sibling.left.color = _BLACK
                self._rotate_right(node.parent)

        case1(startnode)
