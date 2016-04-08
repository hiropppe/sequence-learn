#!/bin/bash

rm -rf ./cv && mkdir cv

python cv_split.py 5 cv

for i in `seq 0 1 4`;
do
  echo "[Cross Validation #$i]"
  echo "Convert to CoNLL format ..."
  ./conv_conll.sh ./cv/${i}/train/ train.txt [0-9]{4}
  ./conv_conll.sh ./cv/${i}/test/ test.txt [0-9]{4}
  echo "Generate features ..."
  cat ./cv/${i}/train/train.txt | ./feature/ner.py > ./cv/${i}/train.crfsuite.txt
  cat ./cv/${i}/test/test.txt   | ./feature/ner.py > ./cv/${i}/test.crfsuite.txt
  echo "Train CRF model ..."
  crfsuite learn -m ./cv/${i}/model -l -L ./cv/${i}/train.log ./cv/${i}/train.crfsuite.txt
  #crfsuite learn -e2 ./cv/${i}/train.crfsuite.txt ./cv/${i}/test.crfsuite.txt
  echo "Evaluate CRF model ..."
  crfsuite tag -qt -m ./cv/${i}/model ./cv/${i}/test.crfsuite.txt > ./cv/${i}/evaluate.log
done

cat ./cv/*/evaluate.log | python eval_all.py
