# -*- coding:utf-8 -*-

from __future__ import division

import time

import numpy as np
import pycrfsuite as crf

from sklearn.cross_validation import KFold
from sklearn.grid_search import ParameterGrid

from metrics import f1_score

class GridSearch(object):
  
  def __init__(self, param_searches, param_base={}, cv=5, scorer=f1_score, model=None):
    self.param_searches = param_searches
    self.param_base = param_base
    self.cv = cv
    self.scorer = scorer
    self.model = model
    self.graphical_model = 'crf1d'
    
    self.best_score = .0
    self.best_algorithm = 'lbfgs'
    self.best_param = {}

  def search(self, X, y, verbose):
    for param_search in self.param_searches:
      if '__best_parameter' in param_search.keys() and param_search['__best_parameter']:
        self.param_base = self.best_param.copy()

      if param_search.keys()[0] in {'lbfgs', 'l2sgd', 'ap', 'pa', 'arow'}:
        for algorithm, param_gs in param_search.items():
          self.search_grid(X, y, algorithm, param_gs, verbose)
      else:
        self.search_grid(X, y, algorithm, param_search, verbose)
    
    if self.model:
      trainer = crf.Trainer(verbose)
      trainer.select(self.best_algorithm, self.graphical_model)
      trainer.set_params(self.best_param)
      for xseq, yseq in zip(X, y):
        trainer.append(xseq, yseq)
      trainer.train(model)

  def search_grid(self, X, y, algorithm, param_grid, verbose):
    param_grid = ParameterGrid({p[0]: p[1] for p in param_grid.items() if not p[0].startswith('__')})          
    for param in param_grid:
      trainer = crf.Trainer(verbose=verbose)
      param_train = self.param_base.copy()
      param_train.update(param)
      trainer.select(algorithm, self.graphical_model)
      trainer.set_params(param_train)
      
      if isinstance(self.cv, int):
        cv = KFold(n=len(X), n_folds=self.cv, shuffle=True, random_state=None)
      
      print('Parameter: (%s) %s' % (algorithm, param_train))
      cv_score = []
      for j, indices in enumerate(cv):
        X_train, y_train = X[indices[0]], y[indices[0]]
        X_test, y_test = X[indices[1]], y[indices[1]]
              
        for xseq, yseq in zip(X_train, y_train):
          trainer.append(xseq, yseq)
        start = time.time()
        trainer.train('model')
        fit_elapsed_in_sec = time.time() - start
        trainer.clear()
              
        tagger = crf.Tagger()
        tagger.open('model')
        start = time.time()
        y_pred = [tagger.tag(xseq) for xseq in X_test]
        predict_elapsed_in_sec = time.time() - start
        tagger.close()
        score = self.scorer(y_pred, y_test, tags_discard={'O'})
        
        print('  cv(%i): score %.4f, train size %i, test size %i, train elapsed %.4f sec, test elapsed %.4f sec' %
                          (j, score, X_train.shape[0], X_test.shape[0], fit_elapsed_in_sec, predict_elapsed_in_sec))
        cv_score.append(score)

      score = np.mean(cv_score)
      if self.best_score < score:
        self.best_score = score
        self.best_param = param_train
        self.best_algorithm = algorithm
      del cv_score[:]
