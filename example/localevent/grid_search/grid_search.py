#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import division

import sys
import codecs

import numpy as np

from sqlearn.crfsuite import crfutils
from sqlearn.crfsuite import ner
from sqlearn.crfsuite.grid_search import GridSearch
from sqlearn.crfsuite.metrics import accuracy, recall, precision, f1_score

if __name__ == '__main__':
  X, y, sent, sent_label = [], [], [], []
  for line in codecs.open('data.conll', 'r', 'utf-8'):
    line = line.strip('\n')
    if line.strip() == '':
      sent.append('\n')
      for item in crfutils.readiter(sent, ['w', 'pos'], ' '):
        ner.feature_extractor(item)
        X.append(item)
        y.append(sent_label)
      sent = []
      sent_label = []
    else:
      splited_line = line.split(' ')
      sent.append('%s %s' % (splited_line[0], splited_line[1]))
      sent_label.append(splited_line[2])

  # process last sent if exists
  if sent:
    sent.append('\n')
    for item in crfutils.readiter(sent, ['w', 'pos'], ' '):
      ner.feature_extractor(item)
      X.append(item)
      y.append(sent_label)

  X = [[feature['F'] for feature in sent] for sent in X]

  X = np.asarray(X)
  y = np.asarray(y)

  base_param = {
    'feature.minfreq': 0,
    'feature.possible_states': False,
    'feature.possible_transitions': False
  }

  search_param = [
    {
      'c1_lbfgs': {
        '__algorithm': 'lbfgs',
        'c1': [1e-4, 1e-3, 0.01, 0.1, 1.],
        'c2': [0.]
      },
      'c2_lbfgs': {
        '__algorithm': 'lbfgs',
        'c1': [0.],
        'c2': [1e-4, 1e-3, 0.01, 0.1, 1.]
      },
      'l2sgd': {
        '__algorithm': 'l2sgd',
        'c2': [1e-4, 1e-3, 0.01, 0.1, 1.]
      }
    },
    {
      '__best_parameter': True,
      'feature.minfreq': [0, 1], 
      'feature.possible_states': [True, False],
      'feature.possible_transitions': [True, False]
    }
  ]

  gs = GridSearch(search_param, base_param, cv=3)
  gs.search(X, y, verbose=False)

  print('Best score: %.4f' % gs.best_score)
  print('Best algorithm: %s' % gs.best_algorithm)
  print('Best params: %s' % gs.best_param)
