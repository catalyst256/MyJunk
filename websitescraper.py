#!/usr/bin/env python

# This requires PhantomJS and the Selinium python drivers

import sys
import hashlib
from selenium import webdriver
# import logging
# logging.basicConfig(level=logging.INFO, filename='scraper.log', format='%(asctime)s %(message)s')

def scrape_website(url):
  try:
    print url
    m = hashlib.md5(url).hexdigest()
    print m
    service_args = ['--ignore-ssl-errors=true']
    br = webdriver.PhantomJS(service_args=service_args, service_log_path='service_scraper.log')
    print br
    br.set_window_size(1024, 768)
    br.get(url)
    print br.get(url)
    filename = m + '.png'
    print filename
    br.save_screenshot(filename)
    br.quit()
    print filename
  except Exception as e:
    # logging.info(str(url) + ': ' + str(e))
    print str(e)
    # sys.exit(1)

if __name__ == '__main__':
  
  if len(sys.argv) != 2:
    print 'Usage: ./websitescraper.py URL'
    print 'Example: ./websitescraper.py http://www.dodgydomain.com'
    sys.exit(1)

  url = sys.argv[1]
  scrape_website(url)



