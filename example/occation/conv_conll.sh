ls ${1} | grep -oP 9[0-9]{4}\(?=\.ann\) | while read id;
do
  python ../../scripts/tagging data/${id}.raw data/${id}.ann >> ${1}/${2}
done

