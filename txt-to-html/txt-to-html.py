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


empty_lines = Suppress( Optional( White('\n')))

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

# interleaving characters with spaces for use in oneOf()
decor_chars_with_spaces = reduce(lambda x,y: x + " " + y, decor_chars)

# TODO: I REALLY need to work on this one, because it have to define
# what's on inside and outside of any of decorated_exprs
undecorated_expr = Combine( CharsNotIn(decor_chars + ' \t\r\n')
                            + ZeroOrMore( Word(decor_chars)
                                          + CharsNotIn(decor_chars + ' \t\r\n')))
                                        
# ' \t\r\n' its "Space Train" for remembering ;) 2010-08-25, 20:06 CEST

#fallback_match = oneOf(decor_chars_with_spaces)
#fallback_expr = fallback_match + ~( CharsNotIn( decor_chars + '\r\n') + matchPreviousExpr(fallback_match))

fallback_exprs = [Group( Literal(char) * 2
                         | (Literal(char) + CharsNotIn(decor_chars + " \t\r\n")))
                  for char in decor_chars]


# Decorated text can be recursive so we need to use Forward()
# to declare body later
decorated_exprs = [Forward() for _ in decors_mapping]


## URL:
## Has two variants: one for matching http://* urls,
## second one for matching local files such as asdf.png or qwer/asdf.png .
## URLs cannot be followed by !, if so, should be just cited.
url = Suppress( White(' \t')) \
    + ( Combine( Literal("http://") + CharsNotIn(' \t\r\n!'))
        | Combine( Optional("http://") 
                 + OneOrMore( CharsNotIn(' \t\r\n.') + ".")
                 + CharsNotIn(' \t\r\n!.\\'))) + ~Literal("!")

# This is what can be contained in any line of text,
# undecorated or decorated text.
inline_atom = ( undecorated_expr
                | reduce(lambda x,y: x | y, decorated_exprs)
                | reduce(lambda x,y: x | y, fallback_exprs)) \
              + Optional(url)

def decorate_with_url(item):
    if len(item) == 2:
        return [['<a href="' + reduce(lambda x,y: x + y, item[1]) + '">',
                 item[0],
                 '</a>']]

inline_atom.setParseAction(decorate_with_url)

inline_expr = OneOrMore(inline_atom + Optional(White(' \t')))

# Lets push into decorated_exprs expressions of
# delimiter + zero or more inline_atom's + delimiter.
# Note that inline_expr is recursively refering to all of 
# decorated_expr's.

def decorate(item):
    tag = decors_mapping[item[0]]
    if tag ==  None:
        return [item[1:-1]]
    else:
        return [["<%s>" % tag] + item[1:-1] + ["</%s>" % tag]]

for index, char in enumerate(decor_chars):
    decorated_exprs[index] << char + inline_expr + char
    decorated_exprs[index].setParseAction(decorate)

#pprint(inline_expr.parseString("* s/*d* - [ ]-/f- add as/df.com -sf *").asList())
test_exprs = ["w@er as*d*f.asdf uip http://asdfwefw/sadfsa/ -*/ a q/w.er /*-",
              "&asdf @@ asdf&",
              "@asdf",
              "@http://@"#,
              #"@_@",
              #"@@@"
              ]
for t in test_exprs:
    pprint(inline_expr.parseString(t).asList())


## Header:
## Will match to a single line that starts with a continuous sequence 
header = LineStart() + Word('*') + inline_expr + Suppress( Optional('\n'))

def do_header(item):
    tag = "h%d" % (len(item[0]) + 1)
    return ["<%s>" % tag, item[1:], "</%s>" % tag]

header.setParseAction(do_header)

roll_stack = [1]


unordered_list = Forward()
ordered_list = Forward()

any_list = unordered_list ^ ordered_list

unordered_elem = "-" + Group(inline_expr) + Optional(any_list)
ordered_elem = "#" + Group(inline_expr) + Optional(any_list)

def do_list_elem(item):
    pass
#roll_elem = ordered_elem | unordered_elem

unordered_list << indentedBlock(unordered_elem, roll_stack, True)
ordered_list << indentedBlock(ordered_elem, roll_stack, True)

ordered_list_first_level = indentedBlock(ordered_elem, roll_stack, False)
unordered_list_first_level = indentedBlock(unordered_elem, roll_stack, False)

roll_block = OneOrMore(ordered_list_first_level | unordered_list_first_level )

# simple approach:
list_item = Forward()
list_item << oneOf("- #") + inline_expr \
             + Optional( indentedBlock(list_item, roll_stack)

pprint(roll_block.parseString("""- asdf
- -qwer-
  # uiop asdfas
- werew sadf a
 - bnm asdfa
 -ghjkl
   -456789
     -789
# asdf
""").asList())

roll_stack.

pprint(roll_block.parseString("""- item one
  # asdf
    - uiop
  # qwer
- item two
  - subitem of "item two", identation matters.
    - obvious.
  # obviously there can be numbered lists.
  # they start with hash mark.""").asList())

### old rolls:
roll_elem = Group( Optional( White(' \t')) + oneOf("- #") + ~( Literal(">")) + inline_expr)
roll_block = OneOrMore( roll_elem + Suppress( Optional('\n')))

def do_roll(item):
    tag_stack = []
    for line in item:
        pass

# Bandwidth-saving maniacs will kill me for this makeblog_ prefixes :P
paragraph_classes = {'=>': 'makeblog_box makeblog_box_right',
                     '<=': 'makeblog_box makeblog_box_left',
                     '->': 'makeblog_right',
                     '|' : 'makeblog_center'}

paragraph_decors = reduce(lambda x,y: x + " " + y, paragraph_classes)

paragraph = ~(oneOf(">> << @@")) + Optional( oneOf("=> <= -> |")) \
    + OneOrMore(~(oneOf(">> << @@")) + inline_expr + Optional('\n'))

def do_paragraph(item):
    first_elem = item[0]
    if type(first_elem) == str:
        pclass = paragraph_classes.get(first_elem)
    else:
        pclass =  None
    if pclass:
        return ['<p class="%s">' % pclass, item[1:], '</p>']
    else:
        return ['<p>', item.asList(), '</p>']

paragraph.setParseAction(do_paragraph)

### Blockquote:

embeddable = Group(paragraph | roll_block)

blockquote = LineStart() + Literal(">>") + Suppress( White('\r\n'))\
             + ZeroOrMore(embeddable + empty_lines) \
             + Literal("<<")

def do_blockquote(item):
    return ["<blockquote>", item[1:-1], "</blockquote>"]

blockquote.setParseAction(do_blockquote)

pprint(blockquote.parseString(""">>

ASDF
QWER

/Albert Einstein/

=> efwe

- asdf
  # sadf
- werwe
<<

>>
asdf
asdf
sad
<<""").asList())

### Code:
"@@"

"@@"

code_block = LineStart() + Literal("@@") + Suppress( White('\r\n')) \
             + OneOrMore( ~Literal("@@") + CharsNotIn('\r\n') + White('\r\n')) \
             + LineStart() + Literal("@@")

def do_code_block(item):
    return ["<pre>", item[1:-1], "</pre>"]

code_block.setParseAction(do_code_block)

pprint(code_block.parseString("""@@
sdf a
  sdf as   
  as 
  as df
@@
 asdf

@@

qwer""").asList())

#### Document Layout:

document = title + empty_lines + attr_map  + empty_lines \
    + ZeroOrMore \
    (
      Group
      (
        header
        | blockquote
        | code_block
        | embeddable
      ) + empty_lines
    ) 

#print document.verify()
#sadf = document.parseString(input_text)
#pprint(sadf.asList())
