#!/bin/bash
touch errors
for n in `seq 10 10 50`
do
  python ./error_by_size.py $n >> errors
done

cat errors | python plot.py
