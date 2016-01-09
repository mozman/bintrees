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

from bintrees import RBTree as PTree
from bintrees import FastRBTree as FTree, has_fast_tree_support

COUNT = 100

setup_RBTree_ps = """
from __main__ import keys, rb_prev, rb_succ
"""
setup_FastRBTree_ps = """
from __main__ import keys, crb_prev, crb_succ
"""

try:
    fp = open('testkeys.txt')
    keys = eval(fp.read())
    fp.close()
    bskeys = zip(keys, keys)
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

ptree = PTree.from_keys(keys)
ftree = FTree.from_keys(keys)


def rb_prev():
    for key in keys:
        try:
            item = ptree.prev_item(key)
        except KeyError:
            pass


def rb_succ():
    for key in keys:
        try:
            item = ptree.succ_item(key)
        except KeyError:
            pass


def crb_prev():
    for key in keys:
        try:
            item = ftree.prev_item(key)
        except KeyError:
            pass


def crb_succ():
    for key in keys:
        try:
            item = ftree.succ_item(key)
        except KeyError:
            pass


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))


def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print ("Nodes: %d" % len(keys))

    shuffle(keys)

    t = Timer("rb_prev()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'PythonTree prev')

    t = Timer("rb_succ()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'PythonTree succ')

    t = Timer("crb_prev()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastXTree prev')

    t = Timer("crb_succ()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastXTree succ')


if __name__ == '__main__':
    if not has_fast_tree_support():
        print("Cython extension for FastRBTree is NOT working.")
    else:
        print("Cython extension for FastRBTree is working.")
    main()
