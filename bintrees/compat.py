#!/usr/bin/env python
#coding:utf-8
# Author:   mozman
# Purpose:
# Created: 09.04.2011
# Copyright (C) , Manfred Moitzi
# License: GPLv3

import sys

PY3 = sys.version_info[0] > 2

def cmp(a, b):
    if a < b:
        return -1
    elif a > b:
        return +1
    else:
        return 0
