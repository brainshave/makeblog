# generate index
INDEXED_TARGETS += 

ALL_TARGETS += $(OUTDIR)/archive.html

$(INDEXED_TARGETS) : $(TMPDIR)

$(OUTDIR)/archive.html : $(TMPDIR) $(INDEXED_TARGETS)
	python indexer/indexer.py $(INDEXED_TARGETS) -o $@
