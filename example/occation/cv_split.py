#!/usr/bin/env python

from __future__ import division

import sys
import os
import glob
import random
import math
import shutil

args = sys.argv

cv = int(args[1]) if 1 < len(args) else 10
work_dir = args[2] if 2 < len(args) else 'cv'

all_files = glob.glob('data/*.ann')
random.shuffle(all_files)

test_size = math.trunc(len(all_files)/cv)
test_files = []
all_set = set(all_files)
for i in xrange(cv):
  test_files = all_files[i*test_size:(i+1)*test_size-1]
  train_set = set(all_set) - set(test_files)
  train_files = list(train_set)
  
  cv_dir = os.path.join(work_dir, str(i))
  cv_train_dir = os.path.join(cv_dir, 'train')
  cv_test_dir = os.path.join(cv_dir, 'test')
  os.mkdir(cv_dir)
  os.mkdir(cv_train_dir)
  os.mkdir(cv_test_dir)

  for train_file in train_files:
    shutil.copy2(train_file, cv_train_dir)
    shutil.copy2(train_file.replace('.ann', '.txt'), cv_train_dir.replace('.ann', '.txt'))
  
  for test_file in test_files:
    shutil.copy2(test_file, cv_test_dir)  
    shutil.copy2(test_file.replace('.ann', '.txt'), cv_test_dir.replace('.ann', '.txt'))

