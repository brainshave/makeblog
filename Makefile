# Main Makeblog's Makefile.

# This file is intended to be included in your project's
# Makefile. Simplest usage of Makeblog looks just like:
# include ../makeblog/Makefile

# Set Makeblog's path for further invocations of make
export MAKEBLOG_PATH = $(dir $(lastword $(MAKEFILE_LIST)))

# This is main index file that lists all posts. Only markdown files
# that have 'date' header set are considered posts. Others are
# considered static pages.
export INDEX = tmp/index.json

# All markdown files will be parsed to json files in tmp dir and
# indexed. JSONS variable is not exported because nested make
# invocations are expected to figure out jsons file paths on their
# own.
export MARKDOWNS = $(wildcard src/*.md)
JSONS = $(patsubst src/%.md,tmp/%.json,$(MARKDOWNS))

.PHONY: blog clean apply_mustache

# Main target.
blog : tmp $(JSONS) $(INDEX) apply_mustache

# Invokes makefile for applying mustache templates.
apply_mustache: $(INDEX)
	$(MAKE) -f $(MAKEBLOG_PATH)/apply_mustache.mk

# First invokes clean for apply_mustache.mk file, so all files that
# are not known here but generated there are properly deleted. It's a
# good practice to clean project in reverse order that it was built.
clean:
	$(MAKE) -f $(MAKEBLOG_PATH)/apply_mustache.mk clean
	rm -rf tmp

# Recreate tmp dir if needed.
tmp:
	mkdir tmp

# Rule for converting markdowns to jsons. Last parameter passed to
# script is path of final html file generated for this markdown
# file. It's needed only to set metadata in json file. No html file is
# generated at this stage.
tmp/%.json : src/%.md
	node $(MAKEBLOG_PATH)/markdown_to_html.js $< $@ $(patsubst tmp/%.post.json,%.html,$@)

# Rule for generating index. Side effect of this is that for every tag
# (defined in 'tag' header in each markdown file) a file named
# <tag>.index.json is generated.
#
# Depenedence on $(JSONS) makes sure that all jsons for pages are
# already generated. Thanks to that running make with -j (jobs)
# parameter is safe.
$(INDEX) : $(JSONS)
	node $(MAKEBLOG_PATH)/indexer.js $@ tmp $?
