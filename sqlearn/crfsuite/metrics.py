# -*- coding:utf-8 -*-

from __future__ import division

import numpy as np

from itertools import chain

from sklearn.preprocessing import LabelBinarizer

def accuracy(y_gold, y, tags={}, tags_discard={}):
  y_gold, y, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _accuracy(y_gold, y, class_indices.values())

def recall(y_gold, y, tags={}, tags_discard={}):
  y_gold, y, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _recall(y_gold, y, class_indices.values())

def precision(y_gold, y, tags={}, tags_discard={}):
  y_gold, y, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _precision(y_gold, y, class_indices.values())

def f1_score(y_gold, y, tags={}, tags_discard={}):
  y_gold, y, class_indices = binarize_y(y_gold, y, tags, tags_discard)
  return _f1(y_gold, y, class_indices.values()) 

def binarize_y(y_gold, y, tags={}, tags_discard={}):
  lb = LabelBinarizer()
  y_gold = lb.fit_transform(list(chain.from_iterable(y_gold)))
  y = lb.transform(list(chain.from_iterable(y)))
  tagset = tags if tags else set(lb.classes_) - tags_discard
  tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
  class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
  return y_gold, y, class_indices  

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
  return np.sum(y_eval[:, indices] == 2)/np.sum(y[:, indices] == 1)

def _f1(y_gold, y, indices):
  recall = _recall(y_gold, y, indices)
  precision = _precision(y_gold, y, indices)
  if not recall + precision:
    return 0
  return 2*recall*precision/(recall+precision)
