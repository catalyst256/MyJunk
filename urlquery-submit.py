#!/usr/bin/env python

# Python goodness to submit URL to URLQuery.net and wait for the report ID.

import sys
import json
import time
import requests

def submit_url(url):
  try:
    payload = {'method': 'submit', 'url': url, 'useragent': 'SneakersInc', 'referer': ''}
    u = 'https://urlquery.net/api/v2/post.php'
    r = requests.post(u, data=payload)
    time.sleep(5)
    json_data = json.loads(r.text)
    q_id = json_data['queue_id']
    return q_id
  except Exception as e:
    print r.text
    sys.exit(1)

def check_url(q_id):
  try:
    payload = {'method': 'queue_status', 'queue_id': q_id}
    u = 'https://urlquery.net/api/v2/post.php'
    r = requests.post(u, data=payload)
    json_data = json.loads(r.text)
    status = json_data['status']
    return status
  except Exception as e:
    print str(e)

def get_report(q_id):
  try:
    payload = {'method': 'queue_status', 'queue_id': q_id}
    u = 'https://urlquery.net/api/v2/post.php'
    r = requests.post(u, data=payload)
    json_data = json.loads(r.text)
    report = json_data['report_id']
    report_url = 'https://urlquery.net/report.php?id=' + str(report)
    return report_url
  except Exception as e:
    print str(e)

if __name__ == '__main__':

  if len(sys.argv) != 2:
    print 'Usage: ./urlquery-submit.py URL'
    print 'Example: ./urlquery-submit.py www.dodgydomain.com'
    sys.exit(1)
  
  url = sys.argv[1]
  # Submit the URL and then check it's progress
  x = submit_url(url)
  finished = 0
  while finished == 0:
    s = check_url(x)
    if 'done' not in s:
      time.sleep(20)
      print s
    else:
      finished += 1
      print get_report(x)

