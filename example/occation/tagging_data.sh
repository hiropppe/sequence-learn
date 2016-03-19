rm -f corpus.iob2
ls data/ | grep -oP [0-9]{4}\(?=\.ann\) | while read id;
do
  echo $id
  #python ../scripts/tagging data/${id}.raw data/${id}.ann
  python ../scripts/tagging data/${id}.raw data/${id}.ann >> corpus.iob2
done

