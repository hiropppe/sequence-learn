# -*- coding: utf-8 -*-

from __future__ import print_function

import sys, codecs

import MeCab
mecab = MeCab.Tagger()

encoding = 'utf-8'

#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def tagging(rawfile, annfile):
  # sort annotations by left position
  ann_lines = sorted(open(annfile, 'r').readlines(), key=lambda x: int(x.split()[2]))
  ann_index = 0

  node_left = 0
  for line in open(rawfile, 'r'):
    node = mecab.parseToNode(line)
    node = node.next

    pre_tag = None
    pre_iob = 'O'
    
    while node:
      tag = None
      iob = 'O'
      
      if len(ann_lines) == 0:
        ann_left = 0
        ann_right = 0
      else:
        ann = ann_lines[ann_index].split()
        ann_left  = int(ann[2])
        ann_right = int(ann[3])
      
      node_right = node_left + len(node.surface.decode(encoding))

      if ann_left <= node_left and node_right <= ann_right:
        tag = ann[1]
        if pre_iob == 'O' or not pre_tag == tag:
          iob = 'B'
        else:
          iob = 'I'

        pre_tag = tag
        pre_iob = iob
      elif ann_right < node_left and ann_index < len(ann_lines) - 1:
        ann_index += 1
      else:
        pass

      label = iob + '-' + tag if tag else iob
      features = node.feature.split(',')
      pos0 = features[0]
      pos1 = features[1]
      pos2 = features[2]
      
      #sys.stdout.write('%s %s %s\n' % (node.surface, pos0, label))
      sys.stdout.write('%s %s_%s %s\n' % (node.surface, pos0, pos1, label))
      #sys.stdout.write('%s %s_%s_%s %s\n' % (node.surface, pos0, pos1, pos2, label))

      node_left = node_right
      # increment wakati space
      node_left += 1
      node_right += 1
      
      node = node.next
  
  sys.stdout.write('\n')
