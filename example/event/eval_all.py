#!/usr/bin/env python

from __future__ import division

import sys

from collections import defaultdict

tags = [
  'O',
  'B-OCCATION',
  'I-OCCATION',
  'B-DATE',
  'I-DATE',
  'B-DATE_PERIOD',
  'I-DATE_PERIOD',
  'B-LOCATION',
  'I-LOCATION',
  'B-ADDRESS',
  'I-ADDRESS',
  'B-TIME_PERIOD',
  'I-TIME_PERIOD',
#  'B-POSTAL_ADDRESS',
#  'I-POSTAL_ADDRESS',
#  'B-URL',
#  'I-URL',
#  'B-PHONE_NUMBER',
#  'I-PHONE_NUMBER',
#  'B-FEE',
#  'I-FEE',
]

label_stats = defaultdict(lambda: [0, 0, 0])
for line in sys.stdin:
  if line.split()[0][:-1] in tags:
    cols = line.split()
    tag = cols[0][:-1]
    num_match = int(cols[1].replace('(', '').replace(',', ''))
    num_model = int(cols[2].replace(',', ''))
    num_ref = int(cols[3].replace(')', ''))
    label_stats[tag][0] += num_match
    label_stats[tag][1] += num_model
    label_stats[tag][2] += num_ref

sys.stdout.write('Performance by label (#match, #model, #ref) (acc, precision, recall, F1):\n')

total_match, total_model, total_ref = 0, 0, 0
o_match, o_model, o_ref = 0, 0, 0
occ_match, occ_model, occ_ref = 0, 0, 0
for tag in tags:
  num_match = label_stats[tag][0]
  num_model = label_stats[tag][1]
  num_ref = label_stats[tag][2]
  pre = 0 if num_model == 0 else num_match/num_model
  rec = 0 if num_ref == 0 else num_match/num_ref
  sys.stdout.write('  %s: (%i, %i, %i) (%.4f, %.4f, %.4f)\n' % 
                    (tag, num_match, num_model, num_ref, pre, rec, 0 if pre+rec == 0 else 2*pre*rec/(pre+rec)))

  total_match += num_match
  total_model += num_model
  total_ref += num_ref
  
  if tag == 'O':
    o_match += num_match
    o_model += num_model
    o_ref += num_ref

  if tag in ['B-OCCATION', 'I-OCCATION']:
    occ_match += num_match
    occ_model += num_model
    occ_ref += num_ref

pre = total_match/total_model
rec = total_match/total_ref

sys.stdout.write('Total: (%i, %i, %i) (%.4f, %.4f, %.4f)\n' % 
                    (total_match, total_model, total_ref, pre, rec, 2*pre*rec/(pre+rec)))

total_match -= o_match
total_model -= o_model
total_ref -= o_ref

pre = total_match/total_model
rec = total_match/total_ref

sys.stdout.write('Total(exclude O): (%i, %i, %i) (%.4f, %.4f, %.4f)\n' % 
                    (total_match, total_model, total_ref, pre, rec, 2*pre*rec/(pre+rec)))

total_match -= occ_match
total_model -= occ_model
total_ref -= occ_ref

pre = total_match/total_model
rec = total_match/total_ref

sys.stdout.write('Total(exclude O, I-OCCATION, B-OCCATION): (%i, %i, %i) (%.4f, %.4f, %.4f)\n' % 
                    (total_match, total_model, total_ref, pre, rec, 2*pre*rec/(pre+rec)))
