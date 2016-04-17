#!/usr/bin/env python
import sys
import os
import shutil
import MySQLdb as my

ann_data_path = sys.argv[1]
train_data_path = sys.argv[2]

if not os.path.exists(train_data_path):
  os.mkdir(train_data_path)

conn = my.connect(
      host='192.168.88.166',
      port=3306,
      db='crawl',
      user='mysql',
      passwd='',
      charset='utf8'
    )

cursor = conn.cursor()

sql = """
  select _id from Corpus where status = 9 order by _id
"""

cursor.execute(sql)

row = cursor.fetchone()
while row:
  shutil.copy2(os.path.join(ann_data_path, str(row[0]).zfill(5) + '.ann'), train_data_path)
  shutil.copy2(os.path.join(ann_data_path, str(row[0]).zfill(5) + '.txt'), train_data_path)
  row = cursor.fetchone()
