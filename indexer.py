#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file COPYING
#
# This part:
# General indexer
# rest of arguments are filenames

import sys, os, getopt, datetime, locale, re, cgi
from string import Template
from pprint import pprint

def print_help():
    print """Cache file indexer.
Indexes cache files that contains metadata about output files.
Cache files are in form of a Python dictionary.
Fields used for now are:
  - date: datetime object,
  - output: file to point to in index (archive listing),
  - title: title for link

Options:
  -o output file for archive
  -i output file for index
  -l output name to the latest entry
  -t template to use for archive
  -m template to use for index
  -a atom output

Rest of parameters are cache files to parse.
"""
    exit(1)


## HEADER FORMAT, modify it to suit your taste:
header_format = '<h2 class="archive_month">%B %Y</h2>'

## load locale defaults from OS:
locale.setlocale(locale.LC_ALL, '')

opts, filenames = getopt.gnu_getopt(sys.argv[1:], 'o:t:l:m:i:a:h')
options = dict(opts)

output_file = options['-o']
output_index_file = options['-i']

template = Template(open(options.get('-t', "templates/article.html")).read())
template_index = Template(open(options.get('-m', "templates/article.html")).read())
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
        

body += '</ul>'

## Writing archive
substitutions = {'title': os.environ['BLOG_ARCHIVE_TITLE'],
                 'body': body,
                 'date': '', #datetime.datetime.now().strftime(os.environ['BLOG_DATE_FORMAT']),
                 'blog_title': os.environ['BLOG_TITLE'],
                 'blog_author': os.environ['BLOG_AUTHOR'],
                 'blog_email': os.environ['BLOG_EMAIL'],
                 'blog_archive_title': os.environ['BLOG_ARCHIVE_TITLE'],
                 'blog_url': os.environ['BLOG_URL']}
open(options['-o'], 'w').write(template.safe_substitute(substitutions))

## Writing index
latest = metadata[0]
latest_content = open(latest['dumpfile']).read()

substitutions.update({'title': latest['title'],
                      'body': latest_content,
                      'date': latest['date'].strftime(os.environ['BLOG_DATE_FORMAT'])})

open(options['-i'], 'w').write(template_index.safe_substitute(substitutions))


entry_template = Template("""
  <entry>
    <title>$title</title>
    <link href="$blog_url/$output" rel="alternate" />
    <id>$blog_url/$output</id>
    <updated>$updated</updated>
    <published>$published</published>
    <content type="html">$body</content>
  </entry>
""")
#2003-12-13T08:29:29-04:00
atom_date_format = "%Y-%m-%dT%H:%M:%SZ"

def make_entry(meta):
    entry_body = cgi.escape(open(meta['dumpfile']).read())
    entry_subs = {'title': meta['title'],
                  'output': meta['output'],
                  'body': entry_body,
                  'published': meta['date'].strftime(atom_date_format),
                  'updated': meta['date'].strftime(atom_date_format),
                  'blog_url': os.environ['BLOG_URL']}
    entry = entry_template.substitute(entry_subs)
    return entry
    
#pprint(map(make_entry, metadata[:10]))

atom_template = Template("""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>$blog_title</title> 
  <link href="$blog_url" rel="self" />
  <updated>$updated</updated>
  <author> 
    <name>$blog_author</name>
  </author>
  <id>$blog_url/$atom_output</id>
  $entries
</feed>
""")

atom_output = options['-a']

atom_entries = reduce(lambda x,y: str(x) + str(y),
                      map(make_entry, metadata[:10]))
atom_subs = {'blog_title': os.environ['BLOG_TITLE'],
             'blog_author': os.environ['BLOG_AUTHOR'],
             'blog_url': os.environ['BLOG_URL'],
             'atom_output': atom_output,
             'updated': metadata[0]['updated'].strftime(atom_date_format),
             'entries': atom_entries}
open(atom_output, "w").write(atom_template.substitute(atom_subs))
