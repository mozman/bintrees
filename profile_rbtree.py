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

try:
    # compare with Benjamin Saller's really damn fast RBTree implementation
    from bsrbtree.rbtree import rbtree as BStree
    do_bstree = True
except ImportError:
    print("Benjamin Sallers RBTrees not available.")
    do_bstree =False

COUNT = 100

setup_RBTree_bd = """
from __main__ import keys, rb_build_delete, RBTree
"""
setup_FastRBTree_bd = """
from __main__ import keys, crb_build_delete, FastRBTree
"""
setup_RBTree_b = """
from __main__ import keys, rb_build, RBTree
"""
setup_FastRBTree_b = """
from __main__ import keys, crb_build, FastRBTree
"""
setup_RBTree_s = """
from __main__ import keys, rb_search, py_searchtree
"""
setup_FastRBTree_s = """
from __main__ import keys, crb_search, cy_searchtree
"""
setup_FastRBTree_swc = """
from __main__ import keys, crb_wc_search, cy_searchtree_wc
"""
setup_BStree_bd = """
from __main__ import keys, bs_build_delete, BStree
"""
setup_BStree_b = """
from __main__ import keys, bs_build, BStree
"""
setup_BStree_s = """
from __main__ import keys, bs_search, BStree, bs_searchtree
"""
setup_BStree_swc = """
from __main__ import keys, bs_wc_search, BStree, bs_searchtree_wc
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
    bs_searchtree_wc = BStree(zip(skeys, skeys))

py_searchtree = RBTree.fromkeys(keys)
cy_searchtree = FastRBTree.fromkeys(keys)
cy_searchtree_wc = FastRBTree.fromkeys(sorted(keys))

def rb_build_delete():
    tree = RBTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def crb_build_delete():
    tree = FastRBTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def rb_build():
    tree = RBTree.fromkeys(keys)

def crb_build():
    tree = FastRBTree.fromkeys(keys)

def rb_search():
    for key in keys:
        obj = py_searchtree[key]

def crb_search():
    for key in keys:
        obj = cy_searchtree[key]

def crb_wc_search():
    for key in keys:
        obj = cy_searchtree_wc[key]

def bs_build_delete():
    tree = BStree(bskeys)
    for key in keys:
        del tree[key]

def bs_build():
    tree = BStree(bskeys)

def bs_search():
    for key in keys:
        obj = bs_searchtree[key]

def bs_wc_search():
    for key in keys:
        obj = bs_searchtree_wc[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("rb_build()", setup_RBTree_b)
    print_result(t.timeit(COUNT), 'RBTree build only')

    t = Timer("crb_build()", setup_FastRBTree_b)
    print_result(t.timeit(COUNT), 'FastRBTree build only')

    if do_bstree:
        t = Timer("bs_build()", setup_BStree_b)
        print_result(t.timeit(COUNT), 'Benjamin Saller RBTree build only')

    t = Timer("rb_build_delete()", setup_RBTree_bd)
    print_result(t.timeit(COUNT), 'RBTree build & delete')

    t = Timer("crb_build_delete()", setup_FastRBTree_bd)
    print_result(t.timeit(COUNT), 'FastRBTree build & delete')

    if do_bstree:
        t = Timer("bs_build_delete()", setup_BStree_bd)
        print_result(t.timeit(COUNT), 'Bejamin Saller RBTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("rb_search()", setup_RBTree_s)
    print_result(t.timeit(COUNT), 'RBTree search')

    t = Timer("crb_search()", setup_FastRBTree_s)
    print_result(t.timeit(COUNT), 'FastRBTree search')

    t = Timer("crb_wc_search()", setup_FastRBTree_swc)
    print_result(t.timeit(COUNT), 'FastRBTree (build tree with sorted key) search')

    if do_bstree:
        t = Timer("bs_search()", setup_BStree_s)
        print_result(t.timeit(COUNT), 'Benjamin Saller RBTree search')

        t = Timer("bs_wc_search()", setup_BStree_swc)
        print_result(t.timeit(COUNT), 'Benjamin Saller RBTree (build tree with sorted key) search')

if __name__=='__main__':
    main()