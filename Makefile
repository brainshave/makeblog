# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# Makefile that makes it all happen

blog: blog_main

# Append to this variable to compile your targets in blog:
ALL_TARGETS = 

# Append files with python dict to include this in archive:
INDEXED_TARGETS += 

INDIR = input
OUTDIR = output
TMPDIR = tmp

-include config

# Include rules from all makefiles in "makefiles" dir:
-include */*.mk
-include */Makefile

#### Indexer part
ALL_TARGETS += $(OUTDIR)/archive.html

$(INDEXED_TARGETS) : $(TMPDIR)

$(OUTDIR)/archive.html : $(TMPDIR) $(INDEXED_TARGETS)
	python indexer/indexer.py $(INDEXED_TARGETS) -o $@

### Main part
blog_main: $(OUTDIR) $(TMPDIR) $(ALL_TARGETS)

$(OUTDIR) $(TMPDIR): 
	mkdir -p $@

clean:
	rm -rf $(OUTDIR)/* $(TMPDIR)
