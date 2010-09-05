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

INDEXED_TARGETS += $(patsubst $(INDIR)/%.txt,$(TMPDIR)/%.html-cache,$(wildcard $(INDIR)/*.txt))

$(HTML_TARGETS) : $(TEMPLATES_DIR)/article.html $(MAKEBLOG_PATH)/txt-to-html/txt-to-html.py $(MAKEBLOG_PATH)/txt-to-html/txt-to-html.mk 

$(TMPDIR)/%.html-cache : $(OUTDIR)/%.html

$(OUTDIR)/%.html : $(INDIR)/%.txt
	python $(MAKEBLOG_PATH)/txt-to-html/txt-to-html.py -i $< -o $@ -c $(patsubst $(INDIR)/%.txt,$(TMPDIR)/%.html-cache,$<) -d $(patsubst $(INDIR)/%.txt,$(TMPDIR)/%.html-dump,$<)
