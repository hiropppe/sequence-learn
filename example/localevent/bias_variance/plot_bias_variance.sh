#!/bin/bash
touch errors
for n in `seq 50 10 500`
do
  python ./error_by_size.py $n >> errors
  sleep 30
done

cat errors | python plot.py
