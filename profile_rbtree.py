#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile RBTree, cRBTree
# Created: 02.05.2010
import sys
from timeit import Timer
from random import shuffle

from bintrees.rbtree import RBTree
from bintrees.crbtree import cRBTree

COUNT = 100

setup_RBTree_bd = """
from __main__ import keys, rb_build_delete, RBTree
"""
setup_cRBTree_bd = """
from __main__ import keys, crb_build_delete, cRBTree
"""
setup_RBTree_b = """
from __main__ import keys, rb_build, RBTree
"""
setup_cRBTree_b = """
from __main__ import keys, crb_build, cRBTree
"""
setup_RBTree_s = """
from __main__ import keys, rb_search, py_searchtree
"""
setup_cRBTree_s = """
from __main__ import keys, crb_search, cy_searchtree
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
except IOError:
    print("create 'testkeys.txt' with profile_rb.py\n")
    sys.exit()

py_searchtree = RBTree.fromkeys(keys)
cy_searchtree = cRBTree.fromkeys(keys)

def rb_build_delete():
    tree = RBTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def crb_build_delete():
    tree = cRBTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def rb_build():
    tree = RBTree.fromkeys(keys)

def crb_build():
    tree = cRBTree.fromkeys(keys)

def rb_search():
    for key in keys:
        obj = py_searchtree[key]

def crb_search():
    for key in keys:
        obj = cy_searchtree[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("rb_build()", setup_RBTree_b)
    print_result(t.timeit(COUNT), 'RBTree build only')

    t = Timer("crb_build()", setup_cRBTree_b)
    print_result(t.timeit(COUNT), 'cRBTree build only')

    t = Timer("rb_build_delete()", setup_RBTree_bd)
    print_result(t.timeit(COUNT), 'RBTree build & delete')

    t = Timer("crb_build_delete()", setup_cRBTree_bd)
    print_result(t.timeit(COUNT), 'cRBTree build & delete')
    # shuffle search keys
    shuffle(keys)
    t = Timer("rb_search()", setup_RBTree_s)
    print_result(t.timeit(COUNT), 'RBTree search')

    t = Timer("crb_search()", setup_cRBTree_s)
    print_result(t.timeit(COUNT), 'cRBTree search')

if __name__=='__main__':
    main()