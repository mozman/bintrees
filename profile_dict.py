#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: profile BinaryTree, cBinaryTree
# Created: 01.05.2010

import sys
from timeit import Timer
from random import shuffle

COUNT = 100

setup_Dict_bd = """
from __main__ import keys, dict_build_delete
"""

setup_Dict_b = """
from __main__ import keys, dict_build
"""

setup_Dict_s = """
from __main__ import keys, dict_search, searchdict
"""

try:
    with open('testkeys.txt') as fp:
        keys = eval(fp.read())
except IOError:
    print("create 'testkeys.txt' with profile_bintree.py\n")
    sys.exit()

searchdict = dict.fromkeys(keys)

def dict_build_delete():
    tree = dict.fromkeys(keys)
    for key in keys:
        del tree[key]

def dict_build():
    tree = dict.fromkeys(keys)

def dict_search():
    for key in keys:
        obj = searchdict[key]

def print_result(time, text):
    print("Operation: {1} takes {0:.2f} seconds\n".format(time, text))

def main():
    print ("Nodes: {0}".format(len(keys)))

    t = Timer("dict_build()", setup_Dict_b)
    print_result(t.timeit(COUNT), 'dict() build only')

    t = Timer("dict_build_delete()", setup_Dict_bd)
    print_result(t.timeit(COUNT), 'dict() build & delete')

    # shuffle search keys
    shuffle(keys)
    t = Timer("dict_search()", setup_Dict_s)
    print_result(t.timeit(COUNT), 'Dict search')

if __name__=='__main__':
    main()