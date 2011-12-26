# Applies mustache template for given LAYOUT variable.

# File name without extension
LAYOUT_NAME = $(notdir $(basename $(LAYOUT)))
# Suffix with dot
LAYOUT_EXT = $(suffix $(LAYOUT))

MUSTACHES = $(patsubst tmp/%.$(LAYOUT_NAME).json,%$(LAYOUT_EXT),$(wildcard tmp/*.$(LAYOUT_NAME).json))

.PHONY: mustaches clean

mustaches: $(MUSTACHES)

clean:
	rm -rf $(MUSTACHES)

%$(LAYOUT_EXT) : tmp/%.$(LAYOUT_NAME).json $(LAYOUT)
	node $(MAKEBLOG_PATH)/apply_mustache.js $(LAYOUT) $< $@
