#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# TXT to HTML converter with nice org-mode-like syntax

import sys, re, getopt, os
from datetime import datetime

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
template = open(options.get('-t', "txt-to-html/article.html")).read()

# read file and split into list of paragraphs
input_text = open(options['-i']).read().expandtabs(8)
paragraphs = re.split('\n\s*\n', input_text)

# title is technically first paragraph,
# so its possible to have multiline titles,
# or subtitles/abstracts. To be considered.
title = paragraphs[0].strip()

def find_attributes(text):
    """
    Find attributes in text.
    "a: b, c, d" is translated to attribute a with value [b,c,d]
    """
    attributes = {}
    for line in text.splitlines():
        attr = re.split(':\s*', line.strip(), 1)
        attributes[attr[0].strip()] = re.split('\s*,\s*', attr[1])
    return attributes

attributes = find_attributes(paragraphs[1])
if len(attributes) != 0 :
    body = paragraphs[2:]
else:
    body = paragraphs[1:] # when first paragraph isn't attribute map

attributes['title'] = title
if not 'date' in attributes:
    attributes['date'] = datetime.fromtimestamp(os.stat(options['-i']).st_mtime)

## Dump attributes to stderr:
if attributes.get('index', 'true') != 'false' and options.get('-c'):
    open(options['-c'], 'w').write(str(attributes))

#### STRUCTURE PARTS PARSERS:
## Each structure part is defined by _expr regular expression
## and function that parses that part.

comments_expr = re.compile(r'^%[^\n]*$', re.MULTILINE)
comments_fn = "" # instead of function just substitute it with text ""

# TODO: To be added later: PARAGRAPHS
#paragraph_expr = re.compile(r'(?:\n|\A).*(?=(?:\n\*)|(

header_expr = re.compile(r'^(\*+)[\t ]*([^\n]*)[\t ]*$', re.MULTILINE)

def header_fn(match):
    # count the stars in first group:
    level = len(match.group(1)) + 1 # one star is h2
    return '<h%d>%s</h%d>' % (level, match.group(2).strip(), level)


# LISTS. expression to distinct listings from others:
list_expr = re.compile(r'((?:\n|\A)[\t ]*[-#](?!>)[\t ]*[^\n]*)+')
# expression to get list items characteristics:
list_item_expr = re.compile(r'^(?P<depth>[\t ]*)(?P<symbol>[-#])(?P<text>.*)$')
def list_fn(match):
    tag_stack = [] # stack of tuples: [ tag, depth_indent ]
    text = ""
    for line in match.group(0).splitlines():
        m = list_item_expr.match(line)
        if m:
            depth = len(m.group("depth"))
            tag = {'-': 'ul', '#': 'ol'}[m.group("symbol")]
            content = m.group("text").strip()
            if len(tag_stack) == 0 or depth > tag_stack[-1][1]:
            	tag_stack.append([tag, depth])
            	text += "<%s>\n" % tag            	
            while depth < tag_stack[-1][1]:
            	old_tag, _ = tag_stack.pop()
            	text += "</%s>\n" % old_tag
            	
            if tag_stack[-1][0] != tag and tag_stack[1][1] == depth:
            	old_tag, _ = tag_stack.pop()
            	tag_stack.append([tag, depth])
            	text += "</%s>\n<%s>\n" % (old_tag, tag)
            
	    text += "<li>%s</li>\n" % content
    tag_stack.reverse()
    for tag, _ in tag_stack:
    	text += "</%s>" % tag
    return text

## BLOCK QUOTES
quotes_expr = re.compile(r'((?:\n|\A)>[^<][^\n]*)+')
def qutoes_fn(match):
    text = "\n<blockquote>"
    for line in match.group(0).splitlines():
    	text += line[1:] + "\n"
    text += "</blockquote>\n"
    return text


#### DECORATIONAL PATTERNS:
## TODO: support all of: http://www.w3schools.com/html5/tag_phrase_elements.asp
decors = [['/', 'em'],
          ['_', 'u'],
	  ['*', 'strong'],
	  ['-', 'del'],
	  ['@', 'code']]
	  
decor_patterns = []
  
for symbol, tag in decors:
    escaped = re.escape(symbol)
    #pattern = re.compile(r"(?<=\s|>)%s\b([^%s]*)\b%s(?=\s|<)" % (escaped, symbol, escaped))
    pattern = re.compile(r"(?<!<|\w)%s(?=\S)([^%s]*)(?<=\S)%s(?=\W)" % (escaped, symbol, escaped))
    bla = tag
    #fn = lambda match: "<%s>%s</%s>" % (bla, match.group(1), tag)
    fn = r"<%s>\1</%s>" % (tag, tag)
    decor_patterns.append([pattern, fn])
	  
#### Merging patterns:
patterns_fns = [[comments_expr, comments_fn],
                [header_expr, header_fn],
                [list_expr, list_fn],
                [quotes_expr, qutoes_fn]]
                
patterns_fns += decor_patterns

#### PROCESS ALL PATTERNS IN ORDER:

body_text = ""
for p in body:
    text = p
    for expr, fn in patterns_fns:
        text = expr.sub(fn,text)
    body_text += text
    
open(options['-o'], 'w').write(template % {'title': title, 'body': body_text})
    
# uncomment to see how patterns look like                
#for pattern, _ in patterns_fns:
#    print >> sys.stderr, pattern.pattern
    

