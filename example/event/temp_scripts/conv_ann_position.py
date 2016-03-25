#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert Wakati annotation to Raw annotation
"""

import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

args = sys.argv

raw_file = args[1]
wakati_file = args[2]
ann_file = args[3]

raw = open(raw_file, 'r').read().decode('utf-8')
wakati = open(wakati_file, 'r').read().decode('utf-8')
ann_lines = sorted(open(ann_file, 'r').readlines(), key=lambda x: int(x.split()[2]))

ann_info = [[y[0], y[1], int(y[2]), int(y[3]), y[4]] for y in [x.decode('utf-8').split() for x in ann_lines]]

raw_pos = 0
wakati_pos = 0
num_wakati_space = 0

ann_pos = 0

def mirumiru(c):
  if c == '\r': return '<CR>'
  if c == '\n': return '<LF>'
  if c == ' ': return '<SPACE>'
  return c

#for ann in ann_info:
#  print ann[0], ann[1], ann[2], ann[3], ann[4]

raw_c_pre = None
while raw_pos < len(raw):
  #print mirumiru(raw[raw_pos]), mirumiru(wakati[wakati_pos]), raw_pos, wakati_pos, num_wakati_space
  raw_c = raw[raw_pos]
  wakati_c = wakati[wakati_pos]
  if not raw_c == wakati_c:
    num_wakati_space += 1
  else:
    raw_pos += 1
  
  wakati_pos += 1
  
  raw_c_pre = raw_c

  ann_line_no = ann_pos / 2
  ann_line_index = ann_pos % 2 + 2

  if ann_line_no < len(ann_info) and ann_info[ann_line_no][ann_line_index] == wakati_pos:
    ann_info[ann_line_no][ann_line_index] = ann_info[ann_line_no][ann_line_index] - num_wakati_space
    ann_pos += 1

for ann in sorted(ann_info, key=lambda x: int(x[0][1:])):
  ann[4] = raw[ann[2]:ann[3]]
  print(u'%s\t%s %i %i\t%s' % (ann[0], ann[1], ann[2], ann[3], ann[4]))
