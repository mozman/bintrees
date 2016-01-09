#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile BinaryTree, FastBinaryTree
# Created: 01.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

from timeit import Timer
from bintrees import BinaryTree
from bintrees import FastBinaryTree, has_fast_tree_support
from random import shuffle

COUNT = 100
KEYS = 5000
KEYRANGE = 1000000

setup_BinaryTree = """
from __main__ import bintree_build_delete, bintree_build, bintree_search, iterbintree
"""
setup_FastBinaryTree = """
from __main__ import cbintree_build_delete, cbintree_build, cbintree_search, itercbintree
"""


def random_keys():
    import random
    return random.sample(range(KEYRANGE), KEYS)
try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
except IOError:
    keys = random_keys()

py_searchtree = BinaryTree.from_keys(keys)
cy_searchtree = FastBinaryTree.from_keys(keys)


def bintree_build_delete():
    tree = BinaryTree.from_keys(keys)
    for key in keys:
        del tree[key]


def cbintree_build_delete():
    tree = FastBinaryTree.from_keys(keys)
    for key in keys:
        del tree[key]


def bintree_build():
    tree = BinaryTree.from_keys(keys)


def cbintree_build():
    tree = FastBinaryTree.from_keys(keys)


def bintree_search():
    for key in keys:
        obj = py_searchtree[key]


def cbintree_search():
    for key in keys:
        obj = cy_searchtree[key]


def iterbintree():
    items = list(py_searchtree.items())


def itercbintree():
    items = list(cy_searchtree.items())


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))


def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print ("Nodes: %d" % len(keys))

    t = Timer("bintree_build()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree build only')

    t = Timer("cbintree_build()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree build only')

    t = Timer("bintree_build_delete()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree build & delete')

    t = Timer("cbintree_build_delete()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("bintree_search()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree search')

    t = Timer("cbintree_search()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree search')

    t = Timer("iterbintree()", setup_BinaryTree)
    print_result(t.timeit(COUNT), 'BinaryTree iter all items')

    t = Timer("itercbintree()", setup_FastBinaryTree)
    print_result(t.timeit(COUNT), 'FastBinaryTree iter all items')

if __name__ == '__main__':
    if not has_fast_tree_support():
        print("Cython extension for FastBinaryTree is NOT working.")
    else:
        print("Cython extension for FastBinaryTree is working.")
    main()
