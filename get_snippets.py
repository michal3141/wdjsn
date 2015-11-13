#!/usr/bin/env python
# encoding: utf-8

from plp import PLP
p = PLP()

VERB = PLP.CZESCI_MOWY.CZASOWNIK

stimulus = u'fajka'
st_forms = set(p.forms(p.rec(u'fajka')[0]))
print st_forms

snippets_count = 0

def parse_file(filename):
    global snippets_count
    with open(filename, 'r') as f:
        all_words = []
        for line in f:
            words = line.strip().split()
            all_words.extend(words)

        stimulus_seen = False
        last_verb = None
        second_to_last_verb = None
        last_verb_index = 0
    
        for i, word in enumerate(all_words):
            word_utf8 = word.decode('utf-8')
            if word_utf8 in st_forms or word_utf8[:-1] in st_forms:
                #print 'stimulus_seen' 
                stimulus_seen = True
            try:
                if p.label(p.rec(word_utf8)[0])[0] == VERB:
                    second_to_last_verb = last_verb
                    last_verb = word_utf8
                    if stimulus_seen:
                        print
                        print
                        for j in xrange(last_verb_index, i+1):
                            print all_words[j],
                        stimulus_seen = False
                        snippets_count += 1
                    last_verb_index = i
                    #print 'verb: ', word
            except:
                pass
                #print 'Issue with %s' % word

def main():
    print '\n## Snippety z NKJP ##'
    parse_file('texts/nkjp_extracted.txt')
    print
    print '\n## Snippety z Lalki Prusa ##'
    parse_file('texts/lalka.txt')
    print
    print '\n## Snippety z Pana Tadeusza ##'
    parse_file('texts/pan_tadeusz.txt')
    print
    print '\n## Snippety z Winnetou ##'
    parse_file('texts/winnetou.txt')
    print
    print '\nZnalezione snippety: %d' % snippets_count

if __name__ == '__main__':
    main()
