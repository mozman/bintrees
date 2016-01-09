#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile big trees
# Created: 15.02.2015
# Copyright (c) 2015 by Manfred Moitzi
# License: MIT License

from timeit import Timer
from random import shuffle

from bintrees import FastRBTree, has_fast_tree_support

COUNT = 1
ITEMS = 2**22

setup_dict = """
from __main__ import dict_build_delete, dict_build, dict_search
"""
setup_FastRBTree = """
from __main__ import crb_build_delete, crb_build, crb_search
"""


keys = [k for k in range(ITEMS)]
shuffle(keys)

fastrbtree_searchtree = FastRBTree.from_keys(keys)
dict_searchtree = dict.fromkeys(keys)


def dict_build_delete():
    d = dict.fromkeys(keys)
    for key in keys:
        del d[key]


def crb_build_delete():
    tree = FastRBTree.from_keys(keys)
    for key in keys:
        del tree[key]


def dict_build():
    d = dict.fromkeys(keys)


def crb_build():
    tree = FastRBTree.from_keys(keys)


def dict_search():
    for key in keys:
        obj = dict_searchtree[key]


def crb_search():
    for key in keys:
        obj = fastrbtree_searchtree[key]


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))


def main():
    print("Nodes: %d" % len(keys))

    t = Timer("dict_build()", setup_dict)
    print_result(t.timeit(COUNT), 'dict build only')

    t = Timer("crb_build()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree build only')

    t = Timer("dict_build_delete()", setup_dict)
    print_result(t.timeit(COUNT), 'dict build & delete')

    t = Timer("crb_build_delete()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("dict_search()", setup_dict)
    print_result(t.timeit(COUNT), 'dict search')

    t = Timer("crb_search()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree search')

if __name__ == '__main__':
    if not has_fast_tree_support():
        print("Cython extension for FastRBTree is NOT working.")
    else:
        print("Cython extension for FastRBTree is working.")
    main()