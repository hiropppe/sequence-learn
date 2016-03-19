#!/usr/bin/env python

import requests
import sys, os, codecs
import extractcontent

extractor = extractcontent.ExtractContent()
extractor.set_option({
    'threshold': 0,
    'min_length': 0
  })

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

for url in sys.stdin:
  try:
    response = requests.get(url[:-1]) 
    content, _ = extractor.analyse(response.content.decode(response.apparent_encoding))
    content = content.strip().replace('\r', '')
    sys.stdout.write(content)
    sys.stdout.flush()
  except Exception, details:
    sys.stderr.write(details)
