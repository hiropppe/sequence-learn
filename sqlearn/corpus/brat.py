# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os
import re
import codecs

import MeCab
mecab = MeCab.Tagger()

import pycrfsuite

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from sqlearn.crfsuite import crfutils
from sqlearn.crfsuite import ner

encoding = 'utf-8'

class Annotator:
  
  def __init__(self, model=None):
    self.tagger = pycrfsuite.Tagger()
    self.tagger.open(model)
  
  def ann(self, text, output=sys.stdout):
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
      
      surface_len = max(len(item[0].decode('utf-8')), 1)

      if pre_iob in ['B', 'I'] and iob in ['B', 'O']:
        output.write('T%i\t%s %s %s\t%s\n' % (tag_index, pre_tag, tag_start, tag_start + tag_offset, text[tag_start:tag_start + tag_offset]))
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
      encoded_sent = sent.encode('utf-8') 
      node = mecab.parseToNode(encoded_sent)
      node = node.next
      while node:
        surface = node.surface
        features = node.feature.split(',')
        parsed_sents.append('%s %s_%s_%s' % (surface, features[0], features[1], features[2]))
        node = node.next
    
    parsed_sents.append('\n')
    
    for X in crfutils.readiter(parsed_sents, ['w', 'pos'], ' '):
      ner.feature_extractor(X)
      yield X

if __name__ == '__main__':
  command = sys.argv[1]
  text_file = sys.argv[2]
  model_file = sys.argv[3]
  
  ann = Annotator(model_file)
  
  text = codecs.open(text_file, 'r', 'utf-8').read().replace(' ', u'　')
  if 'tag' == command:
    for item in ann.tagging(text):
      sys.stdout.write('%s %s\n' % (item[0], item[1]))
  elif 'ann' == command:
    ann.ann(text)
  else:
    pass
