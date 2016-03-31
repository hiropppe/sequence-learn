#!/usr/bin/env python
# -*- coding:utf-8 *+-

import sys, codecs, re
import extractcontent

extractor = extractcontent.ExtractContent()
extractor.set_option({
    'threshold': 0,
    'min_length': 0
  })

sys.stdin = codecs.getwriter('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

re_ctl = re.compile(r'[\x00-\x08\x0d-\x1f]') # [:cntrl:]

text = '\n'.join([line for line in sys.stdin])
text, _ = extractor.analyse(text.decode('utf-8'))
text = text.strip()
text = re_ctl.sub('', text)
text = text.replace(' ', u'　')
sys.stdout.write(text)
sys.stdout.flush()

