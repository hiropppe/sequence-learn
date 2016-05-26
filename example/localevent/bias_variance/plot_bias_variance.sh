#!/bin/bash
touch scores
for n in `seq 390 5 500`
do
  python ./score_by_size.py $n >> scores
  sleep 30
done

cat scores | python plot.py
