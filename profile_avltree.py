#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile AVLTree, FastAVLTree
# Created: 01.05.2010
import sys
from timeit import Timer
from random import shuffle

from bintrees import AVLTree
from bintrees import FastAVLTree
from bintrees import QuickAVLTree

COUNT = 100

setup_AVLTree = """
from __main__ import avl_build_delete, avl_build, avl_search
"""
setup_FastAVLTree = """
from __main__ import cavl_build_delete, cavl_build, cavl_search
"""
setup_QuickAVLTree = """
from __main__ import qavl_build_delete, qavl_build, qavl_search
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

py_searchtree = AVLTree.fromkeys(keys)
cy_searchtree = FastAVLTree.fromkeys(keys)
q_searchtree = QuickAVLTree.fromkeys(keys)

def avl_build_delete():
    tree = AVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def cavl_build_delete():
    tree = FastAVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def qavl_build_delete():
    tree = QuickAVLTree.fromkeys(keys)
    for key in keys:
        del tree[key]

def avl_build():
    tree = AVLTree.fromkeys(keys)

def cavl_build():
    tree = FastAVLTree.fromkeys(keys)

def qavl_build():
    tree = QuickAVLTree.fromkeys(keys)

def avl_search():
    for key in keys:
        obj = py_searchtree[key]

def cavl_search():
    for key in keys:
        obj = cy_searchtree[key]

def qavl_search():
    for key in keys:
        obj = q_searchtree[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    with open('testkeys.txt', 'w') as fp:
        fp.write(repr(keys))
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("avl_build()", setup_AVLTree)
    print_result(t.timeit(COUNT), 'AVLTree build only')

    t = Timer("cavl_build()", setup_FastAVLTree)
    print_result(t.timeit(COUNT), 'FastAVLTree build only')

    t = Timer("qavl_build()", setup_QuickAVLTree)
    print_result(t.timeit(COUNT), 'QuickAVLTree build only')

    t = Timer("avl_build_delete()", setup_AVLTree)
    print_result(t.timeit(COUNT), 'AVLTree build & delete')

    t = Timer("cavl_build_delete()", setup_FastAVLTree)
    print_result(t.timeit(COUNT), 'FastAVLTree build & delete')

    t = Timer("qavl_build_delete()", setup_QuickAVLTree)
    print_result(t.timeit(COUNT), 'QuickAVLTree build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("avl_search()", setup_AVLTree)
    print_result(t.timeit(COUNT), 'AVLTree search')

    t = Timer("cavl_search()", setup_FastAVLTree)
    print_result(t.timeit(COUNT), 'FastAVLTree search')

    t = Timer("qavl_search()", setup_QuickAVLTree)
    print_result(t.timeit(COUNT), 'QuickAVLTree search')

if __name__=='__main__':
    main()