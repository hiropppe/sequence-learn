# -*- coding:utf-8 -*-

from __future__ import division

import numpy as np

from itertools import chain

from sklearn.preprocessing import LabelBinarizer

def scorer(f, tags={}, tags_discard={}):
  return lambda p,g: f(p, g, tags, tags_discard)

def accuracy(y_gold, y, tags={}, tags_discard={}):
  _, _, y_eval, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _accuracy(y_eval, class_indices.values())

def recall(y_gold, y, tags={}, tags_discard={}):
  y_gold, _, y_eval, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _recall(y_gold, y_eval, class_indices.values())

def precision(y_gold, y, tags={}, tags_discard={}):
  _, y, y_eval, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _precision(y, y_eval, class_indices.values())

def f1_score(y_gold, y, tags={}, tags_discard={}):
  y_gold, y, y_eval, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _f1(y_gold, y, y_eval, class_indices.values()) 

def binarize_y(y_gold, y, tags={}, tags_discard={}):
  lb = LabelBinarizer()
  y_gold = lb.fit_transform(list(chain.from_iterable(y_gold)))
  y = lb.transform(list(chain.from_iterable(y)))
  if tags:
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_) if cls in tags}
  elif tags_discard:
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_) if cls not in tags_discard}
  else:
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
  
  return y_gold, y, y_gold + y, class_indices  

def _accuracy(y_eval, indices):
  if not y_eval[:, indices].any():
    return 0
  return np.sum(y_eval[:, indices] == 2)/np.sum(y_eval[:, indices] > 0)

def _recall(y_gold, y_eval, indices):
  if not (y_gold[:, indices].any() and y_eval[:, indices].any()):
    return 0
  return np.sum(y_eval[:, indices] == 2)/np.sum(y_gold[:, indices] == 1)

def _precision(y, y_eval, indices):
  if not (y_eval[:, indices].any() and y[:, indices].any()):
    return 0
  return np.sum(y_eval[:, indices] == 2)/np.sum(y[:, indices] == 1)

def _f1(y_gold, y, y_eval, indices):
  recall = _recall(y_gold, y_eval, indices)
  precision = _precision(y, y_eval, indices)
  if not recall + precision:
    return 0
  return 2*recall*precision/(recall+precision)
