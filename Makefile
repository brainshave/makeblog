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


# INDEXED_TARGETS += 

# ALL_TARGETS += $(OUTDIR)/archive.html



# $(OUTDIR)/archive.html : $(TMPDIR) $(INDEXED_TARGETS)
# 	python indexer/indexer.py $(INDEXED_TARGETS) -o $@



# HTML_TARGETS += $(patsubst $(INDIR)/%.txt,$(OUTDIR)/%.html,$(wildcard $(INDIR)/*.txt))
# ALL_TARGETS += $(HTML_TARGETS)

# INDEXED_TARGETS += $(patsubst $(OUTDIR)/%.html,$(TMPDIR)/%.html-cache,$(HTML_TARGETS))

# $(HTML_TARGETS) : txt-to-html/article.html


# $(INDEXED_TARGETS) : $(TMPDIR)

# $(TMPDIR)/%.html-cache : $(OUTDIR)/%.html
# 	@echo DUPA

# $(OUTDIR)/%.html : $(INDIR)/%.txt
# 	python txt-to-html/txt-to-html.py -i $< -o $@ -c $(patsubst $(OUTDIR)/%,$(TMPDIR)/%-cache,$@)


blog_main: $(OUTDIR) $(TMPDIR) $(ALL_TARGETS)

$(OUTDIR) $(TMPDIR): 
	mkdir -p $@

clean:
	rm -rf $(OUTDIR)/* $(TMPDIR)
