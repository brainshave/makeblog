# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# Compile TXT files to HTML

# Tricky path substitution to generate output/*.html targets from
# input/*.txt sources.
HTML_TARGETS += $(patsubst $(INDIR)/%.txt,$(OUTDIR)/%.html,$(wildcard $(INDIR)/*.txt))
ALL_TARGETS += $(HTML_TARGETS)

INDEXED_TARGETS += $(patsubst $(OUTDIR)/%.html,$(TMPDIR)/%.html-cache,$(HTML_TARGETS))

$(HTML_TARGETS) : templates/article.html

$(TMPDIR)/%.html-cache : $(OUTDIR)/%.html

$(OUTDIR)/%.html : $(INDIR)/%.txt
	python txt-to-html/txt-to-html.py -i $< -o $@ -c $(patsubst $(OUTDIR)/%,$(TMPDIR)/%-cache,$@)
