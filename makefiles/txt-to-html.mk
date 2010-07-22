# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file LICENSE
#
# This part:
# Compile TXT files to HTML

# Tricky path substitution to generate output/*.html targets from
# input/*.txt sources.
HTML_TARGETS := $(patsubst input/%.txt,output/%.html,$(wildcard input/*.txt))
ALL_TARGETS := $(ALL_TARGETS) $(HTML_TARGETS)

$(HTML_TARGETS) : templates/article.html

output/%.html : input/%.txt
	bin/txt-to-html $< > $@
