#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile AVLTree, FastAVLTree
# Created: 01.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

import sys
from timeit import Timer
from random import shuffle

from bintrees import AVLTree, has_fast_tree_support
from bintrees import FastAVLTree

COUNT = 100

setup_AVLTree = """
from __main__ import avl_build_delete, avl_build, avl_search
"""
setup_FastAVLTree = """
from __main__ import cavl_build_delete, cavl_build, cavl_search
"""

try:
    fp = open('testkeys.txt')
    keys = eval(fp.read())
    fp.close()
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

py_searchtree = AVLTree.from_keys(keys)
cy_searchtree = FastAVLTree.from_keys(keys)


def avl_build_delete():
    tree = AVLTree.from_keys(keys)
    for key in keys:
        del tree[key]


def cavl_build_delete():
    tree = FastAVLTree.from_keys(keys)
    for key in keys:
        del tree[key]


def avl_build():
    tree = AVLTree.from_keys(keys)


def cavl_build():
    tree = FastAVLTree.from_keys(keys)


def avl_search():
    for key in keys:
        obj = py_searchtree[key]


def cavl_search():
    for key in keys:
        obj = cy_searchtree[key]


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))


def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print ("Nodes: %d" % len(keys))

    t = Timer("avl_build()", setup_AVLTree)
    print_result(t.timeit(COUNT), 'AVLTree build only')

    t = Timer("cavl_build()", setup_FastAVLTree)
    print_result(t.timeit(COUNT), 'FastAVLTree build only')

    t = Timer("avl_build_delete()", setup_AVLTree)
    print_result(t.timeit(COUNT), 'AVLTree build & delete')

    t = Timer("cavl_build_delete()", setup_FastAVLTree)
    print_result(t.timeit(COUNT), 'FastAVLTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("avl_search()", setup_AVLTree)
    print_result(t.timeit(COUNT), 'AVLTree search')

    t = Timer("cavl_search()", setup_FastAVLTree)
    print_result(t.timeit(COUNT), 'FastAVLTree search')

if __name__ == '__main__':
    if not has_fast_tree_support():
        print("Cython extension for FastAVLTree is NOT working.")
    else:
        print("Cython extension for FastAVLTree is working.")
    main()
