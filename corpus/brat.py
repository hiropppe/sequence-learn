# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import re
import codecs

import MeCab
mecab = MeCab.Tagger()

encoding = 'utf-8'

#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def tagging(rawfile, annfile):
  # sort annotations by left position
  ann_lines = sorted(open(annfile, 'r').readlines(), key=lambda x: int(x.split()[2]))
  ann_index, ann_left, ann_right, node_left, node_right = 0, 0, 0, 0, 0
  
  #text = open(rawfile, 'r').read()
  #raw = text.decode('utf-8')
  raw = codecs.open(rawfile, 'r', encoding).read()
  for line in raw.split('\n'):
    node = mecab.parseToNode(line.encode(encoding))
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
      num_lspace = len(raw[node_left:node_right]) - len(raw[node_left:node_right].lstrip()) 
      node_left += num_lspace

      # Adjust node_right in raw data
      i = 0
      while not re.sub(r'\s', '', raw[node_left:node_right]) == surface:
        print(u'"%s"\t"%s"' % (re.sub(r'\s', '', raw[node_left:node_right]), surface))
        node_right += 1
        i += 1
        if i == 5:
          #break
          raise Exception('err. %s<>%s' % (raw[node_left:node_right].encode(encoding), surface))
      
      if 0 < len(ann_lines):
        if ann_right < node_left and ann_index < len(ann_lines) - 1:
          ann_index += 1
        
        ann = ann_lines[ann_index].split()
        ann_left  = int(ann[2])
        ann_right = int(ann[3])
      
      print(u'%s "%s"\t"%s"\t"%s"' % (' ' in raw[node_left:node_right], raw[node_left:node_right], raw[node_left:node_right].replace(' ', ''), surface))
      print(u'%i %i %i %i' % (ann_left, node_left, node_right, ann_right))
      if not pos0 == 'BOS/EOS' and ann_left <= node_left and node_right <= ann_right:
        tag = ann[1]
        if pre_iob == 'O' or not pre_tag == tag:
          iob = 'B'
        else:
          iob = 'I'

      label = iob + '-' + tag if tag else iob
      
      #sys.stdout.write('%s %s %s\n' % (node.surface, pos0, label))
      sys.stdout.write('%s %s_%s %s\n' % (node.surface, pos0, pos1, label))
      #sys.stdout.write('%s %s_%s_%s %s\n' % (node.surface, pos0, pos1, pos2, label))

      node_left = node_right
      pre_tag = tag
      pre_iob = iob
      
      node = node.next
    
    node_left += 1
    node_right += 1

  sys.stdout.write('\n')
