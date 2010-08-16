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
  -l output name to the latest entry
  -t template to use

Rest of parameters are cache files to parse.
"""
    exit(1)


## HEADER FORMAT, modify it to suit your taste:
header_format = '<h2 class="archive_month">%B %Y</h2>'

## load locale defaults from OS:
locale.setlocale(locale.LC_ALL, '')

opts, filenames = getopt.gnu_getopt(sys.argv[1:], 'o:t:l:h')
options = dict(opts)

output_file = options['-o']

template = Template(open(options.get('-t', "templates/article.html")).read())

# print output_file
#m = re.compile(r'(.*\/+)[^/]*').match(output_file)

metadata = []
for fname in filenames:
    metadata.append(eval(open(fname).read()))

metadata = filter(lambda x: not 'index' in x
                            or not len(x['index']) > 0
                            or not x['index'][0].lower() == 'false',
                  metadata)
metadata.sort(key = lambda x: x['date'], reverse = True)
#### output filename of the latest entry to file given with -l option
if '-l' in options:
    open(options['-l'], 'w').write(metadata[0]['input'])

curr_month = metadata[0]['date']

body = curr_month.strftime(header_format + '<ul class="archive_list">\n')

m = re.compile(r'(.*\/+)[^/]*').match(output_file)
if m:
    outdir = m.group(1)
else:
    outdir = ""

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
                 'date': '', #datetime.datetime.now().strftime(os.environ['BLOG_DATE_FORMAT']),
                 'blog_title': os.environ['BLOG_TITLE'],
                 'blog_author': os.environ['BLOG_AUTHOR'],
                 'blog_email': os.environ['BLOG_EMAIL'],
                 'blog_archive_title': os.environ['BLOG_ARCHIVE_TITLE']}
open(options['-o'], 'w').write(template.safe_substitute(substitutions))
