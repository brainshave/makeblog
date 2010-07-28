# generate index

ALL_TARGETS += $(OUTDIR)/archive.html

$(OUTDIR)/archive.html : $(TMPDIR) $(INDEXED_TARGETS)
	python indexer/indexer.py $(INDEXED_TARGETS) -o $@
