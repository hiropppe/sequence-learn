#!/usr/bin/env python

import sys, codecs
import extractcontent

extractor = extractcontent.ExtractContent()
extractor.set_option({
    'threshold': 0,
    'min_length': 0
  })

sys.stdin = codecs.getwriter('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

text = '\n'.join([line for line in sys.stdin])
text, _ = extractor.analyse(text.decode('utf-8'))
text = text.strip().replace('\r', '')
sys.stdout.write(text)
sys.stdout.flush()

