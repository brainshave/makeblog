#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# General indexer

import sys, os, getopt, datetime
#from datetime import datetime

#print sys.argv
# -o <output file> is only possible option.
# rest of arguments are filenames
opts, filenames = getopt.gnu_getopt(sys.argv[1:], 'o:')

metadata = []
for fname in filenames:
    metadata.append(eval(open(fname).read()))

metadata.sort(key = lambda x: x['date'], reverse = True)

first_date = metadata[1]['date']
curr_year = first_date.year
curr_month = first_date.month
for item in metadata:
    print item['date']
