#!/usr/bin/env python

import requests
import sys
import json

email = sys.argv[1]

def check_email(email):
  try:
    url = 'https://haveibeenpwned.com/api/v2/breachedaccount/'
    req = url + str(email)
    r = requests.get(req, verify=False)
    if r.status_code == 404:
      x = 'Account: ' + email + ' has not been pwned'
      return x
    if r.status_code == 200:
      j = r.json()
      x = json.dumps(j, indent=2, separators=(',', ': '), ensure_ascii=False, encoding="utf-8")
      return x
    else:
      pass
  except Exception as e:
    return str(e)

def check_pastebin(email):
  try:
    url = 'https://haveibeenpwned.com/api/v2/pasteaccount/'
    req = url + str(email)
    r = requests.get(req, verify=False)
    if r.status_code == 404:
      x = 'Account: ' + email + ' has not been pasted'
      return x
    if r.status_code == 200:
      j = r.json()
      x = json.dumps(j, indent=2, separators=(',', ': '), ensure_ascii=False, encoding="utf-8")
      return x
    else:
      pass
  except Exception as e:
    return str(e)


t = check_email(email)
print t
q = check_pastebin(email)
print q