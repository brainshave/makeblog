#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# TXT to HTML converter with nice org-mode-like syntax

import sys, re, getopt, os, locale, cgi
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
    -d path     - dump file (content will be dumped there)
"""
    exit(1)

opts, _ = getopt.gnu_getopt(sys.argv[1:], 't:i:o:c:d:h')
options = dict(opts)

if '-h' in options.keys():
    print_help()

# read page template:
template = Template(open(options.get('-t', "templates/article.html")).read())

# read file and split into list of paragraphs
input_text = open(options['-i']).read()

## A function that merges lists recurseively
def merge_lists(root):
    ret = ""
    for item in root:
        t = type(item)
        if t == str:
            ret += item
        elif t == list:
            ret += merge_lists(item)
        elif item == None:
            pass
        else:
            ret += merge_lists(item.asList())
    return ret


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

def do_attr_map(item):
    return dict([[key.strip(), [i.strip() for i in vals]] for key, vals in item])

attr_map.setParseAction(do_attr_map)

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

line_break = Literal('\\\\')
line_break.setParseAction(lambda: "<br />")

escaped_char = Combine('\\' + Word(decor_chars + "~!", exact=1))
escaped_char.setParseAction(lambda x: x[0][1])

backslash = Literal('\\')

pause = Literal('--')
pause.setParseAction(lambda: "&mdash;")

interpunction_chars = ",.;'[]`!$%^()+={}:\"|<>?"
interpunction = Word(interpunction_chars)

# what's on inside and outside of any of decorated_exprs:
undecorated_expr = Combine( line_break | escaped_char | backslash | pause
                            | interpunction
                            | (CharsNotIn(decor_chars + ' \t\r\n\\' + interpunction_chars)
                               + ZeroOrMore( Word(decor_chars)
                                             + CharsNotIn(decor_chars
                                                          + ' \t\r\n\\'
                                                          + interpunction_chars))))
                                        
# ' \t\r\n' its "Space Train" for remembering ;) 2010-08-25, 20:06 CEST

#fallback_match = oneOf(decor_chars_with_spaces)
#fallback_expr = fallback_match + ~( CharsNotIn( decor_chars + '\r\n') + matchPreviousExpr(fallback_match))

fallback_exprs = [Group( Literal(char) * 2
                         | (Literal(char) + CharsNotIn(decor_chars + " \t\r\n") + interpunction_chars))
                  for char in decor_chars]


# Decorated text can be recursive so we need to use Forward()
# to declare body later
decorated_exprs = [Forward() for _ in decors_mapping]


## URL:
## Has two variants: one for matching http://* urls,
## second one for matching local files such as asdf.png or qwer/asdf.png .
## URLs cannot be followed by !, if so, should be just cited.
url = Suppress( White(' \t')) \
    + Combine( ( Word(alphanums) + "://"
                 #+ OneOrMore( CharsNotIn(' \t\r\n/.') + Optional('.') + FollowedBy(Word(alphanums))) + Word(alphanums) # domain
                 + OneOrMore( CharsNotIn(" \t\r\n" + interpunction_chars+decor_chars)
                              | (Word(interpunction_chars+decor_chars) + ~ (White() | LineEnd()))
                              | "/"))
               | (OneOrMore( CharsNotIn(' \t\r\n.') + "." + ~(White() | LineEnd())) + Word(alphanums)))
    
# This is what can be contained in any line of text,
# undecorated or decorated text.
inline_atom = ( undecorated_expr
                | reduce(lambda x,y: x | y, decorated_exprs)
                | reduce(lambda x,y: x | y, fallback_exprs)) \
              + Optional(url)

def decorate_with_url(item):
    if len(item) == 2:
        if item[0] == "~": # cite url
            return item[1]
        elif item[0] == "!": # cite url inside <a> tag
            content = item[1]
        else:
            content = item[0] # "normal" mode
        return [['<a href="' + reduce(lambda x,y: x + y, item[1]) + '">',
                 content,
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


## Header:
## Will match to a single line that starts with a continuous sequence 
header = LineStart() + Word('*') + inline_expr + Suppress( Optional('\n'))

def do_header(item):
    tag = "h%d" % (len(item[0]) + 1)
    return ["<%s>" % tag, item[1:], "</%s>" % tag]

header.setParseAction(do_header)

### old rolls:
roll_elem = Group( Combine(White(' \t') * (0,1)) + oneOf("- #") + ~( Literal(">")) + inline_expr)
roll_block = OneOrMore( roll_elem + Suppress( Optional('\n')))

def do_roll(item):
    tag_stack = []
    text = []
    for line in item:
        depth = len(line[0].expandtabs(8))
        tag = {'-': 'ul', '#': 'ol'}[line[1]]
        content = line[2:]
        if len(tag_stack) == 0 or depth > tag_stack[-1][1]:
            tag_stack.append([tag, depth])
            text.append("<%s>\n" % tag)

        while depth < tag_stack[-1][1]:
            old_tag, _ = tag_stack.pop()
            text.append("</%s>\n" % old_tag)
            
        if tag_stack[-1][0] != tag and tag_stack[1][1] ==  depth:
            old_tag, _ = tag_stack.pop()
            tag_stack.append([tag, depth])
            text += ["</%s>\n" % old_tag, "<%s>\n" % tag]

        text += ["<li>", content, "</li>\n"]
    tag_stack.reverse()
    for tag, _ in tag_stack:
    	text.append("</%s>" % tag)
    return text

roll_block.setParseAction(do_roll)

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
        return ['<p class="%s">' % pclass, item.asList()[1:], '</p>']
    else:
        return ['<p>', item.asList(), '</p>']

paragraph.setParseAction(do_paragraph)

### Blockquote:

embeddable = Group(roll_block | paragraph)

blockquote = LineStart() + Literal(">>") + Suppress( White('\r\n'))\
             + ZeroOrMore(embeddable + empty_lines) \
             + Literal("<<")

def do_blockquote(item):
    return ["<blockquote>", item.asList()[1:-1], "</blockquote>"]

blockquote.setParseAction(do_blockquote)

### Code:
code_block = LineStart() + Literal("@@") + Suppress( White('\r\n')) \
             + OneOrMore( ~Literal("@@") + CharsNotIn('\r\n') + White('\r\n')) \
             + LineStart() + Literal("@@")

def do_code_block(item):
    code = cgi.escape(merge_lists(item[1:-1]))
    return ["<pre>", code, "</pre>"]

code_block.setParseAction(do_code_block)


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
parsed_tree = document.parseString(input_text, True)
#pprint(parsed_tree.asList())

body_offset = 0
#title = ""
if len(parsed_tree) > 0:
    title = parsed_tree[0]
    body_offset += 1

if len(parsed_tree) > 1:
    attr_map = parsed_tree[1]
    if type(attr_map) == dict:
        attributes = attr_map
        body_offset += 1

attributes['title'] = title
attributes['input'] = options['-i']
attributes['output'] = options['-o']
attributes['dumpfile'] = options.get('-d')
attributes['updated'] = datetime.fromtimestamp(os.stat(options['-i']).st_mtime)

if 'date' in attributes:
    attributes['date'] = datetime.strptime(attributes['date'][0], '%Y-%m-%d')
else:
    attributes['date'] = attributes['updated']
    

## Dump attributes to file given with -c option:
if options.get('-c'):
    open(options['-c'], 'w').write(str(attributes))
    
body_text = merge_lists(parsed_tree[body_offset:])

## Dump body text to file given with -d option:
if options.get('-d'):
    open(options['-d'], 'w').write(body_text)

substitutions = {'title': title,
                 'body': body_text,
                 'date': attributes['date'].strftime(os.environ['BLOG_DATE_FORMAT']),
                 'blog_title': os.environ['BLOG_TITLE'],
                 'blog_author': os.environ['BLOG_AUTHOR'],
                 'blog_email': os.environ['BLOG_EMAIL'],
                 'blog_archive_title': os.environ['BLOG_ARCHIVE_TITLE'],
                 'blog_url': os.environ['BLOG_URL']}

open(options['-o'], 'w').write(template.safe_substitute(substitutions))
