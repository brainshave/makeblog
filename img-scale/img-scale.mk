# AUTHOR:  Szymon Witamborski, santamon@gmail.com
# PROJECT: Makeblog, http://launchpad.net/makeblog
# LICENSE: MIT, included in file COPYING
#
# This part:
# Scale images to desired maximum width
# requires: ImageMagick

MINIATURE_WIDTH ?= 600
MINIATURE_HEIGHT ?= $(MINIATURE_WIDTH)
JPEG_QUALITY ?= 90

#### PNG FILES

# Match all png files in input dir
PNG_TARGETS += $(patsubst $(INDIR)/%,$(OUTDIR)/%,$(wildcard $(INDIR)/*.png))
# Miniatures will have _m suffix
PNG_MINIATURES += $(patsubst $(OUTDIR)/%.png,$(OUTDIR)/%_m.png,$(PNG_TARGETS))

ALL_TARGETS += $(PNG_TARGETS) $(PNG_MINIATURES)

$(PNG_MINIATURES) : $(MAKEBLOG_PATH)/img-scale/img-scale.mk

$(OUTDIR)/%_m.png : $(INDIR)/%.png
	convert $< -depth 16 -gamma 0.454545 -filter lanczos \
		-resize $(MINIATURE_WIDTH)x$(MINIATURE_HEIGHT) \
		-gamma 2.2 -depth 8 $@

$(OUTDIR)/%.png : $(INDIR)/%.png
	cp -a $< $@

#### JPG FILES
JPG_TARGETS += $(patsubst $(INDIR)/%,$(OUTDIR)/%,$(wildcard $(INDIR)/*.jpg))
# Miniatures will have _m suffix
JPG_MINIATURES += $(patsubst $(OUTDIR)/%.jpg,$(OUTDIR)/%_m.jpg,$(JPG_TARGETS))

ALL_TARGETS += $(JPG_TARGETS) $(JPG_MINIATURES)

$(JPG_MINIATURES) : $(MAKEBLOG_PATH)/img-scale/img-scale.mk

$(OUTDIR)/%_m.jpg : $(INDIR)/%.jpg
	convert $< -depth 16 -gamma 0.454545 -filter lanczos \
		-resize $(MINIATURE_WIDTH)x$(MINIATURE_HEIGHT) \
		-gamma 2.2 -depth 8 -quality $(JPEG_QUALITY) -sampling-factor 1x1 $@	

$(OUTDIR)/%.jpg : $(INDIR)/%.jpg
	cp -a $< $@
