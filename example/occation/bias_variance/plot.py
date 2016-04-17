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
  if line == 'Train errors':
    errors = train_errors
  elif line == 'Test errors':
    errors = test_errors
  elif re.match(r'^ [BI]\-', line):
    tag = line.split()[0][:-1]
    err = float(line.split()[1])
    errors[tag].append(err)
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

plot_bias_variance(data_sizes, train_errors, test_errors, ['B-OCCATION', 'I-OCCATION'], 'err_occation.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-LOCATION', 'I-LOCATION'], 'err_location.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-ADDRESS', 'I-ADDRESS'], 'err_address.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-DATE_PERIOD', 'I-DATE_PERIOD'], 'err_dateperiod.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-DATE', 'I-DATE'], 'err_date.png')
plot_bias_variance(data_sizes, train_errors, test_errors, ['B-TIME_PERIOD', 'I-TIME_PERIOD'], 'err_timeperiod.png')
