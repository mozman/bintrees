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

COUNT = 1

setup_RBTree = """
from __main__ import rb_index, rb_item_at
"""
setup_FastRBTree = """
from __main__ import crb_index, crb_item_at
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
    bskeys = zip(keys, keys)
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

pytree = RBTree.fromkeys(keys)
cytree = FastRBTree.fromkeys(keys)

def rb_index():
    for key in keys:
        pytree.index(key)

def rb_item_at():
    for index in xrange(pytree.count):
        pytree.item_at(index)

def crb_index():
    for key in keys:
        cytree.index(key)

def crb_item_at():
    for index in xrange(cytree.count):
        cytree.item_at(index)


def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time, text))

def main():
    fp = open('testkeys.txt', 'w')
    fp.write(repr(keys))
    fp.close()
    print ("Nodes: %d" % len(keys))

    shuffle(keys)

    t = Timer("rb_index()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree index')

    t = Timer("rb_item_at()", setup_RBTree)
    print_result(t.timeit(COUNT), 'RBTree item_at')

    t = Timer("crb_index()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree index')

    t = Timer("crb_item_at()", setup_FastRBTree)
    print_result(t.timeit(COUNT), 'FastRBTree item_at')

if __name__=='__main__':
    main()