cat test.lst | grep ^[^#] | while read line;
do
  set -- ${line}
  echo "Extract [${1}] ${2}"
  echo ${2} | python download.py > data/${1}.download
  cat data/${1}.download | python content.py > data/${1}.raw
  cat data/${1}.raw | mecab -Owakati > data/${1}.txt
done

#find -name '*.txt' | sed -e 's|\.txt|.ann|g' | xargs touch

