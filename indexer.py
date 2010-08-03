#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# General indexer
# rest of arguments are filenames

import sys, os, getopt, datetime, locale, re
from string import Template

def print_help():
    print """Cache file indexer.
Indexes cache files that contains metadata about output files.
Cache files are in form of a Python dictionary.
Fields used for now are:
  - date: datetime object,
  - output: file to point to in index (archive listing),
  - title: title for link

Options:
  -o output file
  -t template to use

Rest of parameters are cache files to parse.
"""
    exit(1)


## HEADER FORMAT, modify it to suit your taste:
header_format = '<h2 class="archive_month">%B %Y</h2>'

## load locale defaults from OS:
locale.setlocale(locale.LC_ALL, '')

opts, filenames = getopt.gnu_getopt(sys.argv[1:], 'o:t:h:')
options = dict(opts)

output_file = options['-o']

template = Template(open(options.get('-t', "templates/article.html")).read())

# print output_file
outdir = re.compile(r'(.*\/+)[^/]*').match(output_file).group(0)

metadata = []
for fname in filenames:
    metadata.append(eval(open(fname).read()))

metadata.sort(key = lambda x: x['date'], reverse = True)

curr_month = metadata[0]['date']

body = curr_month.strftime(header_format + '<ul class="archive_list">\n')

outdir = re.compile(r'(.*\/+)[^/]*').match(output_file).group(1)
### print outdir

for item in metadata:
    curr_day = item['date']
    
    if curr_month.year != curr_day.year \
            or curr_month.month != curr_day.month:
        curr_month = curr_day
        body += curr_month.strftime('</ul>%s<ul class="archive_list">\n' % header_format)

    body += '<li><span class="archive_day">%(day)i</span> ' \
        '<a class="archive_link" href="%(link)s">%(title)s</a></li>\n' % \
        {'title': item['title'], \
         'link': item['output'].replace(outdir, ""), \
         'day': curr_day.day}
        

#item['date'].strftime('%d')

body += '</ul>'
substitutions = {'title': os.environ['BLOG_ARCHIVE_TITLE'],
                 'body': body,
                 'blog_title': os.environ['BLOG_TITLE']}
open(options['-o'], 'w').write(template.safe_substitute(substitutions))
