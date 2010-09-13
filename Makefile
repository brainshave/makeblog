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
BLOG_URL = http://someblog.com
BLOG_ARCHIVE_TITLE = Archives
BLOG_DATE_FORMAT = %Y-%m-%d %A
MAKEBLOG_PATH = .

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
export BLOG_URL
export BLOG_ARCHIVE_TITLE
export BLOG_DATE_FORMAT
export MAKEBLOG_PATH

# Include rules from all makefiles in "makefiles" dir:
-include $(MAKEBLOG_PATH)/*/*.mk
-include $(MAKEBLOG_PATH)/*/Makefile

#### Indexer part, should be executed as a last one
## Generating archive.html
ALL_TARGETS += $(OUTDIR)/archive.html # $(OUTDIR)/index.html

$(ALL_TARGETS) : Makefile config

config :
	touch config

$(INDEXED_TARGETS) : $(TMPDIR)

$(OUTDIR)/archive.html $(OUTDIR)/index.html $(OUTDIR)/atom.xml : $(TMPDIR) $(INDEXED_TARGETS) $(ARCHIVE_TEMPLATE) $(INDEX_TEMPLATE) $(MAKEBLOG_PATH)/indexer.py
	python $(MAKEBLOG_PATH)/indexer.py $(INDEXED_TARGETS) -o $(OUTDIR)/archive.html -t $(ARCHIVE_TEMPLATE) -l $(TMPDIR)/latest -m $(INDEX_TEMPLATE) -i $(OUTDIR)/index.html -a $(OUTDIR)/atom.xml

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
	rm -rf $(ALL_TARGETS) $(TMPDIR) $(OUTDIR)/media
#rm -rf $(OUTDIR)/* $(TMPDIR)
