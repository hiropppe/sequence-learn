rm -f ${1}/${2} && touch ${1}/${2}
ls ${1} | grep -oP ${3}\(?=\.ann\) | while read id;
do
  echo $id
  python ../../scripts/tagging data/${id}.txt data/${id}.ann >> ${1}/${2}
done

