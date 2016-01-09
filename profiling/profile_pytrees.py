#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile pure python trees, works also with ipy
# Created: 01.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

from timeit import Timer
from bintrees import BinaryTree
from bintrees import AVLTree
from bintrees import RBTree

from random import shuffle

COUNT = 100
KEYS = 5000
KEYRANGE = 1000000

setup_BinaryTree_bd = """
from __main__ import keys, bintree_build_delete, BinaryTree
"""
setup_BinaryTree_b = """
from __main__ import keys, bintree_build, BinaryTree
"""
setup_BinaryTree_s = """
from __main__ import keys, bintree_search, py_searchtree
"""
setup_AVLTree_bd = """
from __main__ import keys, avl_build_delete, AVLTree
"""
setup_AVLTree_b = """
from __main__ import keys, avl_build, AVLTree
"""
setup_AVLTree_s = """
from __main__ import keys, avl_search, py_searchtree
"""
setup_RBTree_bd = """
from __main__ import keys, rb_build_delete, RBTree
"""
setup_RBTree_b = """
from __main__ import keys, rb_build, RBTree
"""
setup_RBTree_s = """
from __main__ import keys, rb_search, py_searchtree
"""


def random_keys():
    from random import shuffle, randint
    keys = set()
    while len(keys) < KEYS:
        keys.add(randint(0, KEYRANGE))
    keys = list(keys)
    shuffle(keys)
    return keys
try:
    fp = open('testkeys.txt')
    keys = eval(fp.read())
    fp.close()
except IOError:
    keys = random_keys()

py_searchtree = BinaryTree.from_keys(keys)


def bintree_build_delete():
    tree = BinaryTree.from_keys(keys)
    for key in keys:
        del tree[key]


def bintree_build():
    tree = BinaryTree.from_keys(keys)


def bintree_search():
    for key in keys:
        obj = py_searchtree[key]


def avl_build_delete():
    tree = AVLTree.from_keys(keys)
    for key in keys:
        del tree[key]


def avl_build():
    tree = AVLTree.from_keys(keys)


def avl_search():
    for key in keys:
        obj = py_searchtree[key]


def rb_build_delete():
    tree = RBTree.from_keys(keys)
    for key in keys:
        del tree[key]


def rb_build():
    tree = RBTree.from_keys(keys)


def rb_search():
    for key in keys:
        obj = py_searchtree[key]


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))


def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print ("Nodes: %d" % len(keys))

    t = Timer("bintree_build()", setup_BinaryTree_b)
    print_result(t.timeit(COUNT), 'BinaryTree build only')

    t = Timer("avl_build()", setup_AVLTree_b)
    print_result(t.timeit(COUNT), 'AVLTree build only')

    t = Timer("rb_build()", setup_RBTree_b)
    print_result(t.timeit(COUNT), 'RBTree build only')

    t = Timer("bintree_build_delete()", setup_BinaryTree_bd)
    print_result(t.timeit(COUNT), 'BinaryTree build & delete')

    t = Timer("avl_build_delete()", setup_AVLTree_bd)
    print_result(t.timeit(COUNT), 'AVLTree build & delete')

    t = Timer("rb_build_delete()", setup_RBTree_bd)
    print_result(t.timeit(COUNT), 'RBTree build & delete')

    shuffle(keys)

    t = Timer("bintree_search()", setup_BinaryTree_s)
    print_result(t.timeit(COUNT), 'BinaryTree search')

    t = Timer("avl_search()", setup_AVLTree_s)
    print_result(t.timeit(COUNT), 'AVLTree search')

    t = Timer("rb_search()", setup_RBTree_s)
    print_result(t.timeit(COUNT), 'RBTree search')

if __name__ == '__main__':
    main()