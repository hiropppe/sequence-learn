# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os
import re
import codecs

import MeCab
mecab = MeCab.Tagger()

import pycrfsuite

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from sqlearn.crfsuite import crfutils
from sqlearn.crfsuite import ner

encoding = 'utf-8'
sys.stdout = codecs.getwriter(encoding)(sys.stdout)

re_ctl = re.compile(r'[\x00-\x08\x0d-\x1f]') # [:cntrl:]

def conv_conll(rawfile, annfile):
  # sort annotations by left position
  ann_lines = sorted(open(annfile, 'r').readlines(), key=lambda x: int(x.split()[2]))
  ann_index = -1
  ann_left, ann_right, node_left, node_right = 0, 0, 0, 0
  
  raw = codecs.open(rawfile, 'r', encoding).read()
  if ' ' in raw:
    raise ValueError('Corpus must not contain half space char')

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
      sys.stdout.write(u'%s %s_%s_%s %s\n' % (node.surface.decode(encoding), pos0.decode(encoding), pos1.decode(encoding), pos2.decode(encoding), label))

      node_left = node_right
      pre_tag = tag
      pre_iob = iob
      
      node = node.next
    
    node_left += 1
    node_right += 1

  sys.stdout.write('\n')

class Annotator:
  
  def __init__(self, model=None):
    self.tagger = pycrfsuite.Tagger()
    self.tagger.open(model)
  
  def ann(self, text):
    surface_index = 0
    tag_index, tag_start, tag_offset = 1, 0, 0
    pre_tag = None
    pre_iob = None
    
    for item in self.tagging(text):
      iob = re.findall(r'^([IB])\-', item[1])
      iob = iob[0] if iob else 'O'
      if not iob == 'O':
        tag = re.sub(r'^[IB]\-', '', item[1])
      else:
        tag = None
      
      surface_len = max(len(item[0]), 1)

      if pre_iob in ['B', 'I'] and iob in ['B', 'O']:
        ann = 'T%i\t%s %s %s\t%s' % (tag_index, pre_tag, tag_start, tag_start + tag_offset, text[tag_start:tag_start + tag_offset])
        #output.write('%s\n' % ann)
        yield ann 
        tag_index += 1
      
      if iob == 'B':
        tag_start = surface_index
        tag_offset = 0
      
      tag_offset += surface_len
      surface_index += surface_len
      
      pre_tag = tag
      pre_iob = iob

  def tagging(self, text):
    for item_sequence in self.extract_feature(text):
      F_sequence = [item['F'] for item in item_sequence]
      tags = self.tagger.tag(F_sequence)
      
      for i in xrange(len(item_sequence)):
        yield (item_sequence[i]['w'], tags[i])
  
  def extract_feature(self, text):
    parsed_sents = []
    for sent in text.split('\n'):
      encoded_sent = sent.encode(encoding) 
      node = mecab.parseToNode(encoded_sent)
      node = node.next
      while node:
        surface = node.surface.decode(encoding)
        features = node.feature.decode(encoding).split(',')
        parsed_sents.append('%s %s_%s_%s' % (surface, features[0], features[1], features[2]))
        node = node.next
    
    parsed_sents.append('\n')
    
    for X in crfutils.readiter(parsed_sents, ['w', 'pos'], ' '):
      ner.feature_extractor(X)
      yield X

  def norm(self, text):
    text = text.strip()
    text = re_ctl.sub('', text)
    text = text.replace(' ', u'　')
    return text

# test
if __name__ == '__main__':
  command = sys.argv[1]
  text_file = sys.argv[2]
  model_file = sys.argv[3]
  
  ann = Annotator(model_file)
  
  text = codecs.open(text_file, 'r', 'utf-8').read().replace(' ', u'　')
  text = ann.norm(text)
  
  if 'tag' == command:
    for tag in ann.tagging(text):
      sys.stdout.write('%s %s\n' % (tag[0], tag[1]))
  elif 'ann' == command:
    for ann in ann.ann(text):
      sys.stdout.write('%s\n' % ann)
  else:
    pass
