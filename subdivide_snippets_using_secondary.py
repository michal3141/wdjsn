#!/usr/bin/env python
# encoding: utf-8

__author__ = 'Michal Mrowczyk'

import codecs
import re
from collections import defaultdict
from plp import PLP
p = PLP()

stimulus_list = [u'fajka', u'papieros', u'tytoń', u'dym']
net_files = ['fajka.csv', 'papieros.csv', 'tyton.csv', 'dym.csv']

VERB = PLP.CZESCI_MOWY.CZASOWNIK

def get_net(filenames):
    d = defaultdict(int)
    for filename in filenames:
        with open(filename, 'r') as f:
            for line in f:
                freq, word = line.strip().split(',')
                word = word.decode('utf-8')
                try:
                    bword = p.bform(p.orec(word)[0])
                except:
                    print 'WARNING: Issue with getting baseform for: %s' % word 
                d[bword] += int(freq)
    return d


def subdivide_snippets(filename, d):
    ## Snippet is a key, value is a sum of frequencies from semantic network
    snippets_scores = {}
    with open(filename, 'r') as f:
        for line in f:
            snippets_scores[line] = {}
            snippets_scores[line]['score'] = 0
            snippets_scores[line]['contribs'] = []
            arr = line.strip().split()
            if len(arr) > 0:
                # Getting words in snippet...
                words = _get_words(line.decode('utf-8'))
                # Getting baseforms of this words...
                baseforms = []
                for word in words:
                    try:
                        baseform = p.bform(p.orec(word)[0])
                        baseforms.append(baseform)
                        #print word, baseform
                    except:
                        print 'DEBUG: Issue with getting baseform for: %s' % word
                for baseform in baseforms:
                    if baseform in d:
                        score = d[baseform]
                        snippets_scores[line]['score'] += score
                        snippets_scores[line]['contribs'].append((baseform, score))
    return snippets_scores


def _get_words(line):
    return re.sub("[^\w]", " ",  line, flags=re.UNICODE).split()

def _write(snippet, f):
    f.write(snippet[0].decode('utf-8'))
    f.write(str(snippet[1]['score']))
    f.write(' ')
    for contrib in snippet[1]['contribs']:
        f.write(contrib[0])
        f.write(':')
        f.write(str(contrib[1]))
        f.write(' ')
    f.write('\n')
    f.write('\n')


def main():
    net = get_net(net_files)
    print 'net::', net
    del net['fajka']

    snippets_scores = subdivide_snippets('snippets', net)
    print 'scores::', snippets_scores

    for snippet, score in snippets_scores.iteritems():
        print snippet.decode('utf-8'), score

    sorted_snippets = sorted(snippets_scores.items(), key=lambda x: -x[1]['score'])

    f_paired = codecs.open('paired.txt', mode='w', encoding='utf-8')
    f_unpaired = codecs.open('unpaired.txt', mode='w', encoding='utf-8')
    print
    print '------SNIPPETS SORTED BY WEIGHTS-----'
    print 

    for snippet in sorted_snippets:
        if snippet[1]['score'] > 0:
            _write(snippet, f_paired)
        else:
            _write(snippet, f_unpaired)

        print snippet[0].decode('utf-8'), snippet[1]['score'], snippet[1]['contribs']

    f_paired.close()
    f_unpaired.close()


if __name__ == '__main__':
    main()
