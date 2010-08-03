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

blog: blog_main

# Append to this variable to compile your targets in blog:
ALL_TARGETS = 

# Append files with python dict to include this in archive:
INDEXED_TARGETS += 

INDIR = input
OUTDIR = output
TMPDIR = tmp
TEMPLATES_DIR = templates

# Include config file, so some variables can be overwritten
# by user:
-include config

export BLOG_AUTHOR
export BLOG_EMAIL
export BLOG_TITLE
export BLOG_ARCHIVE_TITLE

# Include rules from all makefiles in "makefiles" dir:
-include */*.mk
-include */Makefile

#### Indexer part, should be executed as a last one
ALL_TARGETS += $(OUTDIR)/archive.html

$(ALL_TARGETS) : Makefile config

config :
	touch config

$(INDEXED_TARGETS) : $(TMPDIR)

ARCHIVE_TEMPLATE = $(TEMPLATES_DIR)/article.html

$(OUTDIR)/archive.html : $(TMPDIR) $(INDEXED_TARGETS) $(ARCHIVE_TEMPLATE)
	python indexer.py $(INDEXED_TARGETS) -o $@ -t $(ARCHIVE_TEMPLATE)

### Main part
blog_main: $(OUTDIR) $(TMPDIR) $(ALL_TARGETS)

$(OUTDIR) $(TMPDIR): 
	mkdir -p $@

clean:
	rm -rf $(OUTDIR)/* $(TMPDIR)
