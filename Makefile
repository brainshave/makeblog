# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# Makefile that makes it all happen

blog: blog_main

# Append to this variable to compile your targets in blog:
ALL_TARGETS = 
INDIR = input
OUTDIR = output
TMPDIR = tmp

-include config

# Include rules from all makefiles in "makefiles" dir:
-include */*.mk
-include */Makefile

blog_main: $(TMPDIR) $(OUTDIR) $(ALL_TARGETS)

$(OUTDIR) $(TMPDIR): 
	mkdir -p $@

clean:
	rm -rf $(ALL_TARGETS)
	rm -rf $(TMPDIR)
