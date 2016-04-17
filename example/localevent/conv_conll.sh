rm -f ${1}/${2} && touch ${1}/${2}
ls ${1} | grep -oP ${3}\(?=\.ann\) | while read id;
#ls data/ | grep '\.ann' | awk 'match($0, /[0-9]+/) {print substr($0, RSTART, RLENGTH)}' | while read id;
do
  #echo "Generate CoNLL Format ${id}"
  python ../../scripts/brat2conll data/${id}.txt data/${id}.ann >> ${1}/${2}
done

