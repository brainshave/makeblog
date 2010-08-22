#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# TXT to HTML converter with nice org-mode-like syntax

import sys, re, getopt, os, locale
from datetime import datetime
from string import Template
from pyparsing import *
from pprint import pprint, PrettyPrinter

locale.setlocale(locale.LC_ALL, '')

def print_help():
    print """TXT to HTML converter, uses org-mode-like syntax.
  
  Options:
    -t path     - use alternative template (default: article.html)
    -i path     - input file
    -o path     - output file
    -c path     - cache file (attributes will go there)
"""
    exit(1)

opts, _ = getopt.gnu_getopt(sys.argv[1:], 't:i:o:c:h')
options = dict(opts)

if '-h' in options.keys():
    print_help()

# read page template:
template = Template(open(options.get('-t', "templates/article.html")).read())

# read file and split into list of paragraphs
input_text = open(options['-i']).read()

ParserElement.setDefaultWhitespaceChars(' \t')

#test cases: empty file, one-line file, 

title = (CharsNotIn('\n') + Suppress('\n') * (0,1)) * (0,None) \
    + Suppress(White())

inline_whitespace = Suppress(White(' \t') * (0,None))

attribute_key = inline_whitespace + CharsNotIn(':\n') + inline_whitespace
attribute_item = inline_whitespace + CharsNotIn(',\n') + inline_whitespace
attribute_list = Group((attribute_item + Suppress(',') * (0,1)) * (0,None))
attribute_row = Group(attribute_key + Suppress(':') + attribute_list + Suppress('\n') * (0,1))
attr_map = Group(attribute_row * (0,None))

document = title + attr_map # + \
    # (
    # header & 
    # blockquote &
    # unordered_list & 
    # ordered_list & 
    # code_block &
    # paragraph
    # ) \
    # * (0,None)
sadf = document.parseString(input_text)
pprint(sadf.asList(), indent=2)
