KINDLEGEN=kindlegen

LEFFF_URL=http://gforge.inria.fr/frs/download.php/file/32626/lefff-ext-3.2.tgz

GEN_FILES := littre.prc dict.html
.DELETE_ON_ERROR:

littre.prc: littre.opf frontmatter.html dict.html
	kindlegen -o $@ $< 

.PHONY: clean
clean:
	@rm -f $(GEN_FILES)
