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
from __main__ import rb_pop_min, rb_pop_max
"""
setup_FastRBTree = """
from __main__ import keys, crb_pop_min, crb_pop_max
"""

try:
    fp = open('testkeys.txt')
    keys = eval(fp.read())
    fp.close()
    bskeys = zip(keys, keys)
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()


def rb_pop_min():
    tree = RBTree.fromkeys(keys)
    while tree.count:
        tree.pop_min()


def rb_pop_max():
    tree = RBTree.fromkeys(keys)
    while tree.count:
        tree.pop_max()


def crb_pop_min():
    tree = FastRBTree.fromkeys(keys)
    while tree.count:
        tree.pop_min()


def crb_pop_max():
    tree = FastRBTree.fromkeys(keys)
    while tree.count:
        tree.pop_max()


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))


def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print("Nodes: %d" % len(keys))

    shuffle(keys)

    t = Timer("rb_pop_min()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree pop_min')

    t = Timer("rb_pop_max()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree pop_max')

    t = Timer("crb_pop_min()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree pop_min')

    t = Timer("crb_pop_max()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree pop_max')

if __name__ == '__main__':
    if not has_fast_tree_support():
        print("Cython extension for FastRBTree is NOT working.")
    else:
        print("Cython extension for FastRBTree is working.")
    main()
