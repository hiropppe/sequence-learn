ls ${1} | grep -oP ${3}\(?=\.ann\) | while read id;
do
  python ../../scripts/tagging data/${id}.raw data/${id}.ann >> ${1}/${2}
done

