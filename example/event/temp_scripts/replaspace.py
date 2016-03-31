#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import codecs

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

for line in sys.stdin:
  cols = line.split('\t')
  sys.stdout.write(u'%s\t%s\t%s' % (cols[0], cols[1], cols[2].replace(u' ', u'　')))
