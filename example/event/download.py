#!/usr/bin/env python

import requests
import sys, codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

for url in sys.stdin:
  response = requests.get(url[:-1]) 
  content = response.content.decode(response.apparent_encoding)
  sys.stdout.write(content)
  sys.stdout.flush()
