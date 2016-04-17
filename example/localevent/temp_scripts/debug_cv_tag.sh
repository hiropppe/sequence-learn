if [ $# -ne 5 ];then
  echo "Usage: sh temp_scripts/debug_cv_tag.sh cv/0/model cv/0/test.crfsuite.txt cv/0/test/test.conll.txt cv/0/test/tagging.txt cv/0/test/tagging_debug.txt"
  exit 1
fi

crfsuite tag -r -m ${1} ${2} > ${4}
python temp_scripts/tagging_diff.py ${4} ${3} > ${5}
