rm -rf data.conv && mkdir data.conv
ls event.20160325 | grep -oP [0-9]+\(?=\.ann\) | while read id;
do
  echo ${id}
  python works/conv_ann_position.py event.20160325/${id}.raw event.20160325/${id}.txt event.20160325/${id}.ann > data.conv/${id}.ann
done

