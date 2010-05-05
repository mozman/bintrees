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

setup_RBTree_ps = """
from __main__ import keys, rb_prev, rb_succ
"""
setup_FastRBTree_ps = """
from __main__ import keys, crb_prev, crb_succ
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
    bskeys = zip(keys, keys)
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

if do_bstree:
    bstree = BStree(bskeys)
pytree = RBTree.fromkeys(keys)
cytree = FastRBTree.fromkeys(keys)


def rb_prev():
    for key in keys:
        try:
            item = pytree.prev_item(key)
        except KeyError:
            pass

def rb_succ():
    for key in keys:
        try:
            item = pytree.succ_item(key)
        except KeyError:
            pass

def crb_prev():
    for key in keys:
        try:
            item = cytree.prev_item(key)
        except KeyError:
            pass

def crb_succ():
    for key in keys:
        try:
            item = cytree.succ_item(key)
        except KeyError:
            pass

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    shuffle(keys)

    t = Timer("rb_prev()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'RBTree prev')

    t = Timer("rb_succ()", setup_RBTree_ps)
    print_result(t.timeit(COUNT), 'RBTree succ')

    t = Timer("crb_prev()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastRBTree prev')

    t = Timer("crb_succ()", setup_FastRBTree_ps)
    print_result(t.timeit(COUNT), 'FastRBTree succ')

if __name__=='__main__':
    main()