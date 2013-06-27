#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: tree walker
# Created: 07.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

class Walker(object):
    __slots__ = ['_node', '_stack', '_tree']

    def __init__(self, tree):
        self._tree = tree
        self._node = tree._root
        self._stack = []

    def reset(self):
        self._stack = []
        self._node = self._tree._root

    @property
    def key(self):
        return self._node.key

    @property
    def value(self):
        return self._node.value

    @property
    def item(self):
        return self._node.key, self._node.value

    @property
    def is_valid(self):
        return self._node is not None

    def goto(self, key):
        self._node = self._tree._root
        while self._node is not None:
            if key == self._node.key:
                return True
            elif key < self._node.key:
                self.go_left()
            else:
                self.go_right()
        return False

    def push(self):
        self._stack.append(self._node)

    def pop(self):
        self._node = self._stack.pop()

    def stack_is_empty(self):
        return len(self._stack) == 0

    def has_child(self, direction):
        if direction == 0:
            return self._node.left is not None
        else:
            return self._node.right is not None

    def down(self, direction):
        if direction == 0:
            self._node = self._node.left
        else:
            self._node = self._node.right

    def go_left(self):
        self._node = self._node.left

    def go_right(self):
        self._node = self._node.right

    def has_left(self):
        return self._node.left is not None

    def has_right(self):
        return self._node.right is not None
