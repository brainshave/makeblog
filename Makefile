# Main makeblog's Makefile.

# Makeblog's path is most likely dir of last loaded Makefile.
export MAKEBLOG_PATH = $(dir $(lastword $(MAKEFILE_LIST)))
export MARKDOWNS = $(wildcard src/*.md)
export INDEX = tmp/index.json
JSONS = $(patsubst src/%.md,tmp/%.json,$(MARKDOWNS))


.PHONY: blog clean apply_mustache

blog : tmp $(JSONS) $(INDEX) apply_mustache

apply_mustache: $(INDEX)
	$(MAKE) -f $(MAKEBLOG_PATH)/apply_mustache.mk

clean:
	$(MAKE) -f $(MAKEBLOG_PATH)/apply_mustache.mk clean
	rm -rf tmp

tmp:
	mkdir tmp

tmp/%.json : src/%.md
	node $(MAKEBLOG_PATH)/markdown_to_html.js $< $@ $(patsubst tmp/%.post.json,%.html,$@)

$(INDEX) : $(JSONS)
	node $(MAKEBLOG_PATH)/indexer.js $@ tmp $(JSONS)
