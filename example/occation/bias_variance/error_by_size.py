#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import division

import numpy as np

import sys
import codecs

from itertools import chain
from collections import defaultdict

from sqlearn.crfsuite import crfutils
from sqlearn.crfsuite import ner

from sklearn import cross_validation
from sklearn.preprocessing import LabelBinarizer

import pycrfsuite as crf

def error_score(y_true, y_pred):
    lb = LabelBinarizer()
    y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
    y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))

    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
    
    y_acc_eval_array = y_true_combined + y_pred_combined
    error_score = {item[0]: 1 - sum(y_acc_eval_array[:, item[1]] == 2)/sum(y_acc_eval_array[:, item[1]] > 0) for item in class_indices.items()}
    
    return error_score

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

X = [[feature['F'] for feature in sent] for sent in X]

X = np.asarray(X)
y = np.asarray(y)

if 1 < len(sys.argv):
  data_size = int(sys.argv[1])
else:
  data_size = len(X) 

k = 3

trainer = crf.Trainer(verbose=False)
trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 50,  # stop earlier
    'num_memories': 3,

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

tagger = crf.Tagger()

train_errors = defaultdict(list)
test_errors = defaultdict(list)

kf = cross_validation.KFold(n=data_size, n_folds=k, shuffle=True, random_state=None)

sys.stderr.write('Split %i dataset into %i consecutive folds\n' % (data_size, k))
for fold_idx, (train_index, test_index) in enumerate(kf):
    sys.stderr.write('Iteration #%i\n' % fold_idx)

    X_train, y_train = X[train_index], y[train_index]
    X_test, y_test = X[test_index], y[test_index]

    # train
    Xy = zip(X_train, y_train)
    for xseq, yseq in Xy:
        trainer.append(xseq, yseq)
    trainer.train('model')
    trainer.clear()

    # predict

    tagger.open('model')
    y_train_pred = [tagger.tag(xseq) for xseq in X_train]
    y_test_pred  = [tagger.tag(xseq) for xseq in X_test]
    tagger.close()

    # evaluate
    train_error = error_score(y_train, y_train_pred)
    test_error = error_score(y_test, y_test_pred)

    map(lambda item: train_errors[item[0]].append(item[1]), train_error.items())
    map(lambda item: test_errors[item[0]].append(item[1]), test_error.items())

sys.stdout.write('#%i\n' % data_size)
sys.stdout.write('Train errors\n')
for item in sorted(train_errors.items(), key=lambda x: ''.join([x[0][2:], x[0][:1]])):
  sys.stdout.write(' %s: %.4f\n' % (item[0], np.mean(item[1])))

sys.stdout.write('Test errors\n')
for item in sorted(test_errors.items(), key=lambda x: ''.join([x[0][2:], x[0][:1]])):
  sys.stdout.write(' %s: %.4f\n' % (item[0], np.mean(item[1])))

