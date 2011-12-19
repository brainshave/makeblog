

MUSTACHES := index.html atom.xml 
MUSTACHES += $(patsubst tmp/%.post.json,%.html,$(wildcard tmp/*.post.json))
MUSTACHES += $(patsubst tmp/%.json,%.html,$(wildcard tmp/*.index.json))
MUSTACHES += $(patsubst tmp/%.json,%.xml,$(wildcard tmp/*.index.json))


.PHONY: mustaches clean

mustaches: $(MUSTACHES)

echo:
	@echo $(MUSTACHES)

clean:
	rm -rf $(MUSTACHES)

%.html : tmp/%.post.json layouts/post.html
	node $(MAKEBLOG_PATH)/apply_mustache.js layouts/post.html $< $@

%.index.html : tmp/%.index.json layouts/index.html
	node $(MAKEBLOG_PATH)/apply_mustache.js layouts/index.html $< $@

%.index.xml : tmp/%.index.json layouts/index.xml
	node $(MAKEBLOG_PATH)/apply_mustache.js layouts/index.xml $< $@

index.html : $(INDEX) layouts/index.html
	node $(MAKEBLOG_PATH)/apply_mustache.js layouts/index.html $< $@

atom.xml : $(INDEX) layouts/index.html
	node $(MAKEBLOG_PATH)/apply_mustache.js layouts/index.xml $< $@
