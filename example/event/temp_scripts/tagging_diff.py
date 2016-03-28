#!/usr/bin/env python

import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

args = sys.argv
# crfsuite tag -r -m data/model data/train.crfsuite.txt > data/test.tagging
tagging_file = codecs.open(sys.argv[1], 'r', 'utf-8')
conll_file = codecs.open(sys.argv[2], 'r', 'utf-8')

conll_lines = conll_file.readlines()
tagging_lines = tagging_file.readlines()

if not len(tagging_lines) == len(conll_lines):
  raise ValueError('illegal input !! %i <> %i' % (len(conll_lines), len(tagging_lines)))

result = zip(conll_lines, tagging_lines)

for w in result:
  if w[1].strip():
    tag_pair = w[1][:-1].split('\t')
    #if not tag_pair[0] == tag_pair[1]:
    sys.stdout.write(u'%s\t%s\n' % (w[0][:-1], tag_pair[1]))
