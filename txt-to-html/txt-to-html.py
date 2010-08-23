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


#test cases: empty file, one-line file, 

#title = Combine( ZeroOrMore( CharsNotIn('\n') + Suppress(Optional('\n')))) \
#    + Suppress( ZeroOrMore('\n'))

# inline_whitespace = Suppress( ZeroOrMore( White(' \t')))

# attribute_key = inline_whitespace + CharsNotIn(':\n') + inline_whitespace
# attribute_item = inline_whitespace + CharsNotIn(',\n') + inline_whitespace
# attribute_list = Group( ZeroOrMore( attribute_item + Suppress( Optional(','))))
# attribute_row = Group( attribute_key + Suppress(':') + attribute_list \
#                            + Suppress(Optional('\n')))
# attr_map = Group( ZeroOrMore( attribute_row))

# styled_line = inline_whitespace + ZeroOrMore(CharsNotIn('\n')) \
#     + inline_whitespace + Suppress( Optional('\n'))

# header = LineStart() + Word('*') + styled_line

# paragraph = OneOrMore(styled_line)


ParserElement.setDefaultWhitespaceChars(' \t')

title = Combine( ZeroOrMore( CharsNotIn('\n') + Suppress( Optional('\n'))))

attr_key = CharsNotIn('\n:')
attr_item = CharsNotIn('\n,')
attr_row = Group( attr_key
                  + Suppress(":")
                  + Group( ZeroOrMore( attr_item 
                                       + Suppress( Optional(",")))))
attr_map = ZeroOrMore( attr_row + Suppress( Optional('\n')))

attr_map.setParseAction(lambda x: dict(x.asList()))

empty_lines = Suppress(Optional( White('\n')))

document = title + empty_lines + attr_map  + empty_lines #\
    # + Suppress(White()) \
    # + ZeroOrMore \
    # (
    #   Group
    #   (
    #     header
    #     # & blockquote
    #     # & code_block
    #     # & unordered_list
    #     # & ordered_list
    #     #| paragraph
    #   ) + Suppress( Optional( '\n'))
    # ) 

#print document.verify()
sadf = document.parseString(input_text)
pprint(sadf.asList())
