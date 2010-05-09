#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile RBTree, FastRBTree
# Created: 02.05.2010
import sys
from timeit import Timer
from random import shuffle

from bintrees import RBTree
from bintrees import FastRBTree
from bintrees import QuickRBTree

try:
    # compare with Benjamin Saller's really damn fast RBTree implementation
    from bsrbtree.rbtree import rbtree as BStree
    do_bstree = True
except ImportError:
    print("Benjamin Sallers RBTrees not available.")
    do_bstree =False

COUNT = 100

setup_RBTree = """
from __main__ import rb_build_delete, rb_build, rb_search
"""
setup_FastRBTree = """
from __main__ import crb_build_delete, crb_build, crb_search
"""
setup_QuickRBTree = """
from __main__ import qrb_build_delete, qrb_build, qrb_search
"""
setup_BStree = """
from __main__ import bs_build_delete, bs_build, bs_search
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
    bskeys = zip(keys, keys)
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

if do_bstree:
    bs_searchtree = BStree(bskeys)
    skeys = list(sorted(keys))

py_searchtree = RBTree.fromkeys(keys)
cy_searchtree = FastRBTree.fromkeys(keys)
q_searchtree = QuickRBTree.fromkeys(keys)

def rb_build_delete():
    tree = RBTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def crb_build_delete():
    tree = FastRBTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def qrb_build_delete():
    tree = QuickRBTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def rb_build():
    tree = RBTree.fromkeys(keys)

def crb_build():
    tree = FastRBTree.fromkeys(keys)

def qrb_build():
    tree = QuickRBTree.fromkeys(keys)

def rb_search():
    for key in keys:
        obj = py_searchtree[key]

def crb_search():
    for key in keys:
        obj = cy_searchtree[key]

def qrb_search():
    for key in keys:
        obj = q_searchtree[key]

def bs_build_delete():
    tree = BStree(bskeys)
    for key in keys:
        del tree[key]

def bs_build():
    tree = BStree(bskeys)

def bs_search():
    for key in keys:
        obj = bs_searchtree[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("rb_build()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree build only')

    t = Timer("crb_build()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree build only')

    t = Timer("qrb_build()", setup_QuickRBTree)
    print_result(t.timeit(COUNT), 'QuickRBTree build only')

    if do_bstree:
        t = Timer("bs_build()", setup_BStree)
        print_result(t.timeit(COUNT), 'Benjamin Saller RBTree build only')

    t = Timer("rb_build_delete()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree build & delete')

    t = Timer("crb_build_delete()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree build & delete')

    t = Timer("qrb_build_delete()", setup_QuickRBTree)
    print_result(t.timeit(COUNT), 'QuickRBTree build & delete')

    if do_bstree:
        t = Timer("bs_build_delete()", setup_BStree)
        print_result(t.timeit(COUNT), 'Benjamin Saller RBTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("rb_search()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree search')

    t = Timer("crb_search()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree search')

    t = Timer("qrb_search()", setup_QuickRBTree)
    print_result(t.timeit(COUNT), 'QuickRBTree search')

    if do_bstree:
        t = Timer("bs_search()", setup_BStree)
        print_result(t.timeit(COUNT), 'Benjamin Saller RBTree search')


if __name__=='__main__':
    main()