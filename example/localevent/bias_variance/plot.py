#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re

from itertools import chain
from collections import defaultdict

import matplotlib.pyplot as plt

data_sizes = []
train_errors = defaultdict(list)
test_errors = defaultdict(list)

for line in sys.stdin:
  line = line[:-1]
  if line == 'Train scores':
    errors = train_errors
    scores = None
  elif line == 'Test scores':
    errors = test_errors
    scores = defaultdict(lambda: defaultdict(list))
  elif re.match(r'^ [BI]\-', line):
    tag = line.split()[0][:-1]
    errors[tag].append(1-float(line.split()[1]))
    if scores:
      scores[tag]['Recall'].append(float(line.split()[2])
      scores[tag]['Precision'].append(float(line.split()[3])
      scores[tag]['F1'].append(float(line.split()[4])
  else: 
    size_m = re.match('^#([0-9]+)$', line)
    if size_m:
      data_sizes.append(int(size_m.group(1)))

def plot_bias_variance(data_sizes, train_errors, test_errors, tags, image):
  plt.figure(num=None, figsize=(6, 5))
  plt.ylim([0.0, 1.0])
  plt.xlabel('Data set size')
  plt.ylabel('Error')
  plt.title("Bias-Variance")
  map(lambda tag: plt.plot(data_sizes, train_errors[tag], data_sizes, test_errors[tag], lw=1), tags)
  plt.legend(list(chain.from_iterable([['%s test error' % tag, '%s train error' % tag] for tag in tags])),
      loc='upper right')
  plt.grid(True, linestyle='-', color='0.75')
  plt.savefig(image)

def plot_score(data_sizes, scores, score_name, tags, image):
  plt.figure(num=None, figsize=(6, 5))
  plt.ylim([0.0, 1.0])
  plt.xlabel('Data set size')
  plt.ylabel('Score')
  plt.title(score_name)
  map(lambda tag: plt.plot(data_sizes, scores[tag][score_name], lw=1), tags)
  plt.legend(tags, loc="upper right")
  plt.grid(True, linestyle='-', color='0.75')
  plt.savefig(image)

plot_bias_variance(data_sizes, train_errors, test_errors, ['B-OCCATION', 'I-OCCATION'], 'err_occation.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-LOCATION', 'I-LOCATION'], 'err_location.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-ADDRESS', 'I-ADDRESS'], 'err_address.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-DATE_PERIOD', 'I-DATE_PERIOD'], 'err_dateperiod.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-DATE', 'I-DATE'], 'err_date.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-TIME_PERIOD', 'I-TIME_PERIOD'], 'err_timeperiod.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-FEE', 'I-FEE'], 'err_fee.png')

plot_score(data_sizes, scores, 'F1', ['B-OCCATION', 'I-OCCATION'], 'f1_occation.png')
plot_score(data_sizes, scores, 'F1', ['B-LOCATION', 'I-LOCATION'], 'f1_location.png')
plot_score(data_sizes, scores, 'F1', ['B-ADDRESS', 'I-ADDRESS'], 'f1_address.png')
plot_score(data_sizes, scores, 'F1', ['B-DATE_PERIOD', 'I-DATE_PERIOD'], 'f1_dateperiod.png')
plot_score(data_sizes, scores, 'F1', ['B-DATE', 'I-DATE'], 'f1_date.png')
plot_score(data_sizes, scores, 'F1', ['B-TIME_PERIOD', 'I-TIME_PERIOD'], 'f1_timeperiod.png')
plot_score(data_sizes, scores, 'F1', ['B-FEE', 'I-FEE'], 'f1_fee.png')
