#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import codecs

import numpy as np

#from sqlearn.crfsuite.grid_search import GridSearch
#from sqlearn.crfsuite.metris import f1_score

import pycrfsuite as crf

X = []
y = []
sent = []
sent_label = []
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

def binarize_y(y_gold, y):
  lb = LabelBinarizer()
  y_gold = lb.fit_transform(list(chain.from_iterable(y_gold)))
  y = lb.transform(list(chain.from_iterable(y)))
        
  tagset = tags if tags else set(lb.classes_) - tags_discard
  tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
  class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
 
  return y_gold, y, class_indices  

def f1_score(y_gold, y, tags={}, tags_discard={}):
  y_gold, y, class_indices = binarize_y(y_gold, y)
  return _f1(y_gold, y, class_indices.values()) 

def _accuracy(y_gold, y, indices):
  y_eval = y_gold + y
  return np.sum(y_eval[:, indices] == 2)/np.sum(y_eval[:, indices] > 0)

def _recall(y_gold, y, indices):
  y_eval = y_gold + y
  return np.sum(y_eval[:, indices] == 2)/np.sum(y_gold[:, indices] == 1)

def _precision(y_gold, y, indices):
  if not y[:, indices].any():
    return 0
  y_eval = y_gold + y
  return np.sum(y_eval[:, index] == 2)/np.sum(y[:, indices] == 1)

def _f1(y_gold, y, indices):
  recall = _accuracy(y_gold, y, indices)
  precision = _precision(y_gold, y, indices)
  if not recall + precision:
    return 0
  return 2*recall*precision/(recall+precision)

base_params = {
  'feature.minfreq': 0,
  'feature.possible_states': False,
  'feature.possible_transitions': False
}

alg_grid = {
  'lbfgs': {
    'c1': numpy.linspace(0, 1, num=5),
    'c2': numpy.linspace(0, 1, num=5),
    'epcilon': numpy.linspace [0, 1, num=5],
    '__max_iterations': 1000
  },
  'l2sgd': {
    'c2': numpy.linspace(0, 1, num=5),
    '__max_iterations': 1000
  }
}

gm_grid = {
  'feature.minfreq': [0, 1, 2], 
  'feature.possible_states': [True, False],
  'feature.possible_transitions': [True, False]
}

class GridSearchCV(object):
  
  def __init__(self, algo='lbfgs', gm='clf1d', base_params={}, cv=5, score=f1_score):
    self.gm = gm
    self.algo = algo
    self.cv = cv
    self.score = score
    self.base_param = base_param

    self.trainer = crf.Trainer(verbose)
    self.trainer.select(self.algo, self.gm)
  
  def search(self, X, y, steps, verbose=False):
    best_score = .0
    for step in steps:

      train_params = {}
      if step.keys()[0] in {'lbfgs', 'l2sgd'}:
        for algo, grid in step.items():
          self.trainer.select(algo)
          
          param_index = {}
          param_position = []
          params = []
          for i, key in enumerate(grid.keys()):
            param_name_index[i] = key
            param_position.append(0)
            params.append(grid[key])

          for i, p in enumerate(param_position):
            train_params[param_index[i]] = params[i][p]
          
          self.trainer.set_params(train_param.update(self.base_param))
          for xseq, yseq in zip(X, y):
            self.trainer.append(xseq, yseq)
          trainer.train('model')
          
      else:
        pass 

gs = GridSearch('crf1d', base_params, cv=5, scorer=f1_score)
best_score, best_algorithm, best_params = gs.train(X, y, steps=[alg_grid, gm_grid], verbose=True)

print('Best score: accuracy:%.4f recall:%.4f precision:%.4f f1:%.4f' % best_score)
print('Best algorithm: %s' % best_algorithm)
print('Best params: %s' % best_params)

trainer = crf.Trainer(best_algorithm, best_params, verbose=True)
for xseq, yseq in zip(X, y):
  trainer.append(xseq, yseq)
trainer.train('model')
