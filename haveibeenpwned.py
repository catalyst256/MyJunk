#!/usr/bin/env python

import requests
import sys
import json

email = sys.argv[1]

def check_email(email):
  url = 'https://haveibeenpwned.com/api/v2/breachedaccount/'
  req = url + str(email)
  print req
  r = requests.get(req, verify=False)
  if r.status_code == 404:
    print 'Account: ' + email + ' has not been pwned'
  if r.status_code == 200:
    j = r.json()
    x = json.dumps(j, indent=2, separators=(',', ': '), ensure_ascii=False, encoding="utf-8")
    print x
  else:
    print r.status_code

def check_pastebin(email):
  url = 'https://haveibeenpwned.com/api/v2/pasteaccount/'
  req = url + str(email)
  print req
  r = requests.get(req, verify=False)
  if r.status_code == 404:
    print 'Account: ' + email + ' has not been pasted'
  if r.status_code == 200:
    j = r.json()
    x = json.dumps(j, indent=2, separators=(',', ': '), ensure_ascii=False, encoding="utf-8")
    print x
  else:
    print r.status_code


check_email(email)
check_pastebin(email)
