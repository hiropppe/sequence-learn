#!/bin/bash
touch errors
for n in `seq 50 5 500`
do
  python ./error_by_size.py $n >> errors
done

cat errors | python plot.py
