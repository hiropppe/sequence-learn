#!/bin/bash
touch errors
for n in `seq 50 5 500`
do
  python ./score_by_size.py $n >> scores
  sleep 30
done

cat scores | python plot.py
