#!/usr/bin/env python

# This requires PhantomJS and the Selinium python drivers

import sys
import hashlib
from selenium import webdriver

def scrape_website(url):
  try:
    m = hashlib.md5(url).hexdigest()
    br = webdriver.PhantomJS()
    br.set_window_size(1024, 768)
    br.get(url)
    filename = m + '.png'
    br.save_screenshot(filename)
    br.quit()
    return filename
  except Exception as e:
    print str(e)
    sys.exit(1)

if __name__ == '__main__':
  
  if len(sys.argv) != 2:
    print 'Usage: ./websitescraper.py URL'
    print 'Example: ./websitescraper.py http://www.dodgydomain.com'
    sys.exit(1)

  url = sys.argv[1]
  print scrape_website(url)



