#!/bin/bash

echo "[CRFSuite Cross Validation]"
echo "Convert to brat to CoNLL format"
./conv_conll.sh ./data/ train.conll.txt
echo "Generate features"
cat ./data/train.conll.txt | python chunking.py > ./data/train.crfsuite.txt
echo "Train CRF model"
crfsuite learn -m ./data/model -l -L ./data/train.log ./data/train.crfsuite.txt
#crfsuite learn -g5 -x -l -L ./data/train.log ./data/train.crfsuite.txt
