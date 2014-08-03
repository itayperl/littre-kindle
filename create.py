#!/usr/bin/env python
# coding: utf-8
import glob
import lxml.etree
import sys
import os
import codecs
import string
import argparse
import pickle
import re
from collections import defaultdict

HEADER = u'''<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <title>Dictionnaire de la langue française par E. Littré</title>
    <style type="text/css">
        .nature {
            font-size: small;
            font-style: italic;
        }
    </style>
  </head>
  <body>
  <mbp:frameset>
  <h3>Note</h3>
  <p>This E-book was generated from the following resources:</p>
  <ul>
      <li><a href="http://www.littre.org">XMLittré</a> - a digitized version of the Littré with semantic mark-up. Licensed under CC BY-SA 3.0</li>
      <li><a href="http://alpage.inria.fr/~sagot/lefff.html">LeFFF</a> - a database of word inflections. Licensed under the Lesser General Public License for Linguistic Resources (available <a href="http://infolingu.univ-mlv.fr/DonneesLinguistiques/Lexiques-Grammaires/lgpllr.html">here</a>).</li>
  </ul>
  <mbp:pagebreak />
'''

FOOTER = '''  </mbp:frameset>
  </body>
</html>
'''

def get_paragraphs(root, options):
    elt_text = lambda e: e.text or ''
    elt_tail = lambda e: e.tail or ''
    text = elt_text(root)

    for e in root.iterchildren():
        if options.compact and e.tag in ('cit', 'rubrique'):
            if text.strip():
                yield text
            text = elt_tail(e)
        elif e.tag in ('cit', 'rubrique', 'indent'):
            if text.strip():
                yield text
            for par in get_paragraphs(e, options):
                yield par
            text = elt_tail(e)
        else:
            text += elt_text(e) + elt_tail(e)

    if text.strip():
        yield text

def write_entries(outfp, xml_fn, inflections, options):
    tree = lxml.etree.parse(xml_fn)
    for entry in tree.getroot().getchildren():
        outfp.write('    <mbp:pagebreak />\n')
        term = entry.attrib['terme']
        sense = entry.attrib.get('sens')

        # "ABORDÉ, ÉE" etc.
        raw_term = term.split(',')[0]
        # TERME (S') / TERME (SE)
        raw_term = re.sub(r"\s+\(S['E]\)", '', raw_term)
        try:
            nature = entry.iter('entete').next().iter('nature').next().text.strip()
        except StopIteration:
            nature = ''
        outfp.write(u'    <idx:entry>\n')

        outfp.write(u'        <idx:orth value="{}">\n'.format(raw_term.lower()))

        cur_infls = set(inflections[term.upper()]) - set([term.upper()])
        if cur_infls:
            outfp.write(u'            <idx:infl>\n')
            for infl in cur_infls:
                outfp.write(u'                <idx:iform value="{}" exact="yes" />\n'.format(infl.lower()))
            outfp.write(u'            </idx:infl>\n')
        outfp.write(u'        </idx:orth>')

        outfp.write(u'{}'.format(term))
        if sense is not None:
            outfp.write(u'<sup>{}</sup>'.format(sense))
        outfp.write(u' <span class="nature">{}</span><br><br>\n'.format(nature))

        for variant in entry.iter('corps').next().iter('variante'):
            outfp.write(u'            <img src="bullet.jpg"/>\n')
            for par in get_paragraphs(variant, options):
                outfp.write(u'                {}<br>\n'.format(par))
            outfp.write(u'            <br>')

        outfp.write(u'    </idx:entry>\n')

def parse_inflections(fp, options):
    d = defaultdict(set)

    for line in fp:
        if not line.strip():
           continue

        infl, _, nature, _, main_entry, _ = line.split('\t', 5)
        if nature not in ('nc', 'np', 'v', 'adv', 'advm', 'advp', 'adj'):
            continue
        if set(infl) & set(string.punctuation):
            continue

        main_entry = main_entry.split('_')[0].upper()

        if options.extra_inflections:
            # TODO X-je (puis-je etc.)
            #      verbe-tu/vous/nous...

            # Spelling reform of 1835: verbal suffix oi* => ai*
            ai_re = re.compile(r'ai(s|t|ent)$')
            if nature == 'v' and ai_re.search(infl):
                d[main_entry].add(ai_re.sub(r'oi\1', infl))

        d[main_entry].add(infl)

    return d

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compact', action='store_true', help='Remove citations, etymologies and so on.')
    parser.add_argument('-e', '--extra-inflections', action='store_true', help='Add some alternative spellings')
    parser.add_argument('--cache', action='store_true', help='Cache parsed lefff')
    parser.add_argument('outfile', help='Output MOBI (PRC) dictionary file name')
    parser.add_argument('xml_dir', help='XMLittré directory')
    parser.add_argument('lefff_file', help='lefff-ext file name')
    args = parser.parse_args()

    cache_fn = '{}.pkl'.format(args.lefff_file)
    if args.cache and os.path.exists(cache_fn):
        with open(cache_fn) as f:
            inflections = pickle.load(f)
    else:
        with codecs.open(args.lefff_file, 'r', 'latin1') as f:
            inflections = parse_inflections(f, args)
        if args.cache:
            with open(cache_fn, 'w') as f:
                pickle.dump(inflections, f)

    with codecs.open(args.outfile, 'w', 'utf-8') as out:
        out.write(HEADER)
        for xml_fn in sorted(glob.glob(os.path.join(args.xml_dir, '*.xml'))):
            write_entries(out, xml_fn, inflections, args)
        out.write(FOOTER)

if __name__ == '__main__':
    main()
