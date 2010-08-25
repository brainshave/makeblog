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

###### Parser start
# Lineends are significant, so setup default whitespace chars
# to space + tab. (default value is " \t\n\r")
ParserElement.setDefaultWhitespaceChars(' \t')

#### Head part

## Title:
## Zero or more lines with some chars that are not \n.
## Empty line won't match, so title will be all first non-emtpy lines.
title = Combine( ZeroOrMore( CharsNotIn('\n') + Suppress( Optional('\n'))))

## Attributes map:
## Block of non-empty lines with syntax:
## attr_key: attr_item1, attr_item2
attr_key = CharsNotIn('\n:')
attr_item = CharsNotIn('\n,')
attr_row = Group( attr_key
                  + Suppress(":")
                  + Group( ZeroOrMore( attr_item 
                                       + Suppress( Optional(",")))))
attr_map = ZeroOrMore( attr_row + Suppress( Optional('\n')))

# Attributes map is converted to dict when parsing:
attr_map.setParseAction(lambda x: dict(x.asList()))

#### Body part

## Header:
## Will match to a single line that starts with a continuous sequence 
header = LineStart() + Word('*') + CharsNotIn('\n') + Suppress( Optional('\n'))


## Decorators:
## Bold text, underline, code and so on.

# decors_mapping is a map of decorated text delimiter to html tag
decors_mapping = {'/': 'em',
                  '_': 'u',
                  '*': 'strong',
                  '-': 'del',
                  '@': 'code',
                  '&': None}

# lets grab all delimiters with one string
decor_chars = reduce(lambda x,y: x+y, decors_mapping.keys())

# TODO: I REALLY need to work on this one, because it have to define
# what's on inside and outside of any of decorated_exprs
undecorated_expr = Combine( CharsNotIn(decor_chars + ' \t\r\n')
                            + ZeroOrMore( Word(decor_chars)
                                          + CharsNotIn(decor_chars + ' \t\r\n')))
                                        
# ' \t\r\n' its "Space Train" for remembering ;) 2010-08-25, 20:06 CEST


# Decorated text can be recursive so we need to use Forward()
# to declare body later
decorated_exprs = [Forward() for _ in decors_mapping]


## URL:
## Has two variants: one for matching http://* urls,
## second one for matching local files such as asdf.png or qwer/asdf.png .
## URLs cannot be followed by !, if so, should be just cited.
url = Suppress( White(' \t')) \
    + ( Group(Literal("http://") + CharsNotIn(' \t\r\n'))
        | Group( Optional("http://") 
                 + OneOrMore( CharsNotIn(' \t\r\n.') + ".")
                 + CharsNotIn(' \t\r\n!.') + ~Literal("!")))

# This is what can be contained in any line of text,
# undecorated or decorated text.
inline_atom = ( undecorated_expr | reduce(lambda x,y: x | y, decorated_exprs)) \
              + Optional(url)

inline_expr = OneOrMore(inline_atom + Optional(White(' \t')))

# Lets push into decorated_exprs expressions of
# delimiter + zero or more inline_atom's + delimiter.
# Note that inline_expr is recursively refering to all of 
# decorated_expr's.

for index, char in enumerate(decor_chars):
    decorated_exprs[index] << Group(char + inline_expr + char)

#pprint(inline_expr.parseString("* s/*d* - [ ]-/f- add as/df.com -sf *").asList())
expr = "w@er as*d*f.asdf uip http://asdfwefw/sadfsa/ -*/ a q/w.er /*-"
expr = "@@"
pprint(inline_expr.parseString(expr).asList())


roll_elem = Group( Optional( White(' \t')) + oneOf("- #") + inline_expr)
roll_block = OneOrMore( roll_elem + Suppress( Optional('\n')))

paragraph = Optional( oneOf("=> <= -> |")) \
    + OneOrMore( inline_expr + Suppress( Optional('\n')))


#### Document Layout:

empty_lines = Suppress( Optional( White('\n')))

document = title + empty_lines + attr_map  + empty_lines \
    + ZeroOrMore \
    (
      Group
      (
        header
        # & blockquote
        # & code_block
        | roll_block
        # unordered_list
        # & ordered_list
        | paragraph
      ) + empty_lines
    ) 

#print document.verify()
sadf = document.parseString(input_text)
pprint(sadf.asList())
