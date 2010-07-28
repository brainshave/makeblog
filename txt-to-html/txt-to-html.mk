# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# Compile TXT files to HTML

# Tricky path substitution to generate output/*.html targets from
# input/*.txt sources.
HTML_TARGETS := $(patsubst $(INDIR)/%.txt,$(OUTDIR)/%.html,$(wildcard $(INDIR)/*.txt))
ALL_TARGETS := $(ALL_TARGETS) $(HTML_TARGETS)

$(HTML_TARGETS) : txt-to-html/article.html

$(OUTDIR)/%.html : $(INDIR)/%.txt
	python txt-to-html/txt-to-html.py -i $< -o $@ -c $(patsubst $(OUTDIR)/%,$(TMPDIR)/%.cache,$@)
