KINDLEGEN := kindlegen
PYTHON    := python

LEFFF_URL := http://gforge.inria.fr/frs/download.php/file/32626/lefff-ext-3.2.tgz
LEFFF_FILE := lefff-ext-3.2/lefff-ext-3.2.txt

XMLITTRE_GIT=https://bitbucket.org/Mytskine/xmlittre-data.git

GEN_FILES := littre.prc dict.html xmlittre lefff.txt
.DELETE_ON_ERROR:

littre.prc: littre.opf frontmatter.html dict.html
	$(KINDLEGEN) -c0 -dont_append_source -verbose -o $@ $< 

dict.html: xmlittre lefff.txt create.py
	$(PYTHON) create.py --cache -ec $@ xmlittre lefff.txt

lefff.txt:
	curl $(LEFFF_URL) | tar --transform 's!.*/!!' -zxf - $(LEFFF_FILE)
	mv $(notdir $(LEFFF_FILE)) $@

xmlittre:
	@rm -rf $@
	git clone $(XMLITTRE_GIT) $@

.PHONY: clean
clean:
	@rm -rf $(GEN_FILES)
