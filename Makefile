# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# Makefile that makes it all happen

# Default configuration, create file 'config' to overwrite it
# in a peaceful manner.
BLOG_AUTHOR = Anonymous Coward
BLOG_EMAIL = me@inter.net
BLOG_TITLE = Makeblog-Made Blog
BLOG_ARCHIVE_TITLE = Archives
BLOG_DATE_FORMAT = %Y-%m-%d %A

blog: blog_main

# Append to this variable to compile your targets in blog:
ALL_TARGETS = 

# Append files with python dict to include this in archive:
INDEXED_TARGETS += 

INDIR = input
OUTDIR = output
TMPDIR = tmp
TEMPLATES_DIR = templates


ARCHIVE_TEMPLATE = $(TEMPLATES_DIR)/article.html
INDEX_TEMPLATE = $(TEMPLATES_DIR)/article.html
# Include config file, so some variables can be overwritten
# by user:
-include config

export BLOG_AUTHOR
export BLOG_EMAIL
export BLOG_TITLE
export BLOG_ARCHIVE_TITLE
export BLOG_DATE_FORMAT

# Include rules from all makefiles in "makefiles" dir:
-include */*.mk
-include */Makefile

#### Indexer part, should be executed as a last one
## Generating archive.html
ALL_TARGETS += $(OUTDIR)/archive.html $(OUTDIR)/index.html

$(ALL_TARGETS) : Makefile config

config :
	touch config

$(INDEXED_TARGETS) : $(TMPDIR)

$(OUTDIR)/archive.html : $(TMPDIR) $(INDEXED_TARGETS) $(ARCHIVE_TEMPLATE) indexer.py
	python indexer.py $(INDEXED_TARGETS) -o $@ -t $(ARCHIVE_TEMPLATE) -l $(TMPDIR)/latest

$(OUTDIR)/index.html : $(TMPDIR) $(OUTDIR)/archive.html $(INDEX_TEMPLATE)
	python txt-to-html/txt-to-html.py -i `cat $(TMPDIR)/latest` -o $@ -t $(INDEX_TEMPLATE)

#### copying media for templates (imgs, csss, fonts...)
TEMPLATE_MEDIA = $(patsubst $(TEMPLATES_DIR)/media/%,$(OUTDIR)/media/%,$(wildcard $(TEMPLATES_DIR)/media/*))

$(OUTDIR)/media/% : $(TEMPLATES_DIR)/media/%
	cp -a $< $@

$(TEMPLATES_DIR)/media :
	mkdir $@

### Main part
blog_main: $(OUTDIR) $(TMPDIR) $(ALL_TARGETS) $(OUTDIR)/media $(TEMPLATE_MEDIA)

$(OUTDIR) $(TMPDIR) $(OUTDIR)/media: 
	mkdir -p $@

clean:
	rm -rf $(OUTDIR)/* $(TMPDIR)
