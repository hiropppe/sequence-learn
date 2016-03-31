# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import re
import codecs

import MeCab
mecab = MeCab.Tagger()

encoding = 'utf-8'

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def tagging(rawfile, annfile):
  # sort annotations by left position
  ann_lines = sorted(open(annfile, 'r').readlines(), key=lambda x: int(x.split()[2]))
  ann_index = -1
  ann_left, ann_right, node_left, node_right = 0, 0, 0, 0
  
  raw = codecs.open(rawfile, 'r', encoding).read()
  if ' ' in raw:
    raise ValueError('Corpus must not contains half space char')

  for line in raw.split('\n'):
    encoded_line = line.encode(encoding)
    node = mecab.parseToNode(encoded_line)
    node = node.next
     
    pre_tag = None
    pre_iob = 'O'
    
    while node:
      tag = None
      iob = 'O'
      
      surface = node.surface.decode(encoding)
      features = node.feature.split(',')
      
      pos0 = features[0]
      pos1 = features[1]
      pos2 = features[2]
      
      node_right = node_left + len(surface)
      
      # Adjust node left in raw data
      #num_lspace = len(raw[node_left:node_right]) - len(raw[node_left:node_right].lstrip()) 
      #node_left += num_lspace

      # Adjust node_right in raw data
      #i = 0
      #while not raw[node_left:node_right] == surface and not re.sub(r'\s', '', raw[node_left:node_right]) == surface:
      #  print(u'1 "%s" "%s" "%s"' % (raw[node_left:node_right], re.sub(r'\s', '', raw[node_left:node_right]), surface))
      #  node_right += 1
      #  i += 1
      #  if i == 5:
      #    raise Exception(u'char sequence not match. %s\t%s' % (raw[node_left:node_right], surface))
      
      if 0 < len(ann_lines):
        if ann_right <= node_left and ann_index < len(ann_lines) - 1:
          ann_index += 1
        
        if not ann_index == -1:
          ann = ann_lines[ann_index].split()
          ann_left  = int(ann[2])
          ann_right = int(ann[3])
      
      #print(u'2 %s "%s"\t"%s"\t"%s"' % (' ' in raw[node_left:node_right], raw[node_left:node_right], raw[node_left:node_right].replace(' ', ''), surface))
      #print(u'3 %i %i %i %i' % (ann_left, node_left, node_right, ann_right))
      if not pos0 == 'BOS/EOS' and ann_left <= node_left and node_right <= ann_right:
        tag = ann[1]
        if pre_iob == 'O' or not pre_tag == tag:
          iob = 'B'
        else:
          iob = 'I'

      label = iob + '-' + tag if tag else iob
      
      #sys.stdout.write(u'%s %s_%s %s\n' % (node.surface.decode(encoding), pos0.decode(encoding), pos1.decode(encoding), label))
      sys.stdout.write('%s %s_%s_%s %s\n' % (node.surface.decode(encoding), pos0.decode(encoding), pos1.decode(encoding), pos2.decode(encoding), label))

      node_left = node_right
      pre_tag = tag
      pre_iob = iob
      
      node = node.next
    
    node_left += 1
    node_right += 1

  sys.stdout.write('\n')
