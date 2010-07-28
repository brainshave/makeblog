# generate index

ALL_TARGETS := $(OUTDIR)/archive.html $(ALL_TARGETS) 

$(OUTDIR)/archive.html : $(TMPDIR) $(INDEXED_TARGETS)
	python indexer/indexer.py $(INDEXED_TARGETS) -o $@
