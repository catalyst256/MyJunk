#!/usr/bin/env python

import requests
import re
import sys
from BeautifulSoup import BeautifulSoup

def lookup_name(name, location):
  details = []
  url = 'http://www.thephonebook.bt.com/publisha.content/en/search/residential/search.publisha?Surname=%s&Location=%s&Initial=&Street=' %(name, location)
  try:
    r = requests.get(url)
    html = r.text
    parsed_html = BeautifulSoup(html)
    x = parsed_html.body.findAll('div', attrs={'class':'recordBody'})
    if len(x) == 0:
      return 'Nothing found'
    else:
      for s in x:
        details.append(s.text.replace('Tel: (', ',').replace(')', '').replace('-Text Number', ',').replace('-Map', '').split(','))
    return details
  except Exception as e:
    return e 

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print 'Usage: ./btphone.py [Surname] [Location]'
    print 'Example: ./btphone.py Bloggs London'
    sys.exit(1)

  name = sys.argv[1]
  location = sys.argv[2]

  x = lookup_name(name, location)
  for i in x:
    print i