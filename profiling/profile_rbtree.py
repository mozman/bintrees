#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile RBTree, FastRBTree
# Created: 02.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

import sys
from timeit import Timer
from random import shuffle

from bintrees import RBTree
from bintrees import FastRBTree, has_fast_tree_support

COUNT = 100

setup_RBTree = """
from __main__ import rb_build_delete, rb_build, rb_search
"""
setup_FastRBTree = """
from __main__ import crb_build_delete, crb_build, crb_search
"""

try:
    fp = open('testkeys.txt')
    keys = eval(fp.read())
    fp.close()
    bskeys = zip(keys, keys)
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

py_searchtree = RBTree.from_keys(keys)
cy_searchtree = FastRBTree.from_keys(keys)


def rb_build_delete():
    tree = RBTree.from_keys(keys)
    for key in keys:
        del tree[key]


def crb_build_delete():
    tree = FastRBTree.from_keys(keys)
    for key in keys:
        del tree[key]


def rb_build():
    tree = RBTree.from_keys(keys)


def crb_build():
    tree = FastRBTree.from_keys(keys)


def rb_search():
    for key in keys:
        obj = py_searchtree[key]


def crb_search():
    for key in keys:
        obj = cy_searchtree[key]


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))


def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print ("Nodes: %d" % len(keys))

    t = Timer("rb_build()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree build only')

    t = Timer("crb_build()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree build only')

    t = Timer("rb_build_delete()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree build & delete')

    t = Timer("crb_build_delete()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("rb_search()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree search')

    t = Timer("crb_search()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree search')

if __name__ == '__main__':
    if not has_fast_tree_support():
        print("Cython extension for FastRBTree is NOT working.")
    else:
        print("Cython extension for FastRBTree is working.")
    main()
