#!/usr/bin/env python

import requests, re, sys

# Add some colouring for printing packets later
YELLOW = '\033[93m' # Yellow is for information
GREEN = '\033[92m' # Green is GOOD, means something worked
END = '\033[0m' # It's the end of the world as we know it
RED = '\033[91m' # Red is bad, means something didn't work

name_res = []
phone_res = []
addr_res = []
url = 'http://www.thephonebook.bt.com/publisha.content/en/search/residential/search.publisha'

if len(sys.argv) != 3:
	print 'Usage is ./btphone [Surname] [Location]'
	print 'Example: ./btphone Bloggs Moon'
	sys.exit(1)

search_name = sys.argv[1]
search_town = sys.argv[2]

name_search = 'recordTitle">.(\S.*)</div>'
phone_search = 'class="phone">Tel:.(\S.*)</span>.-.<'
address_search = '<div>(\S.*).-.<a href="map'

query = url + '?Surname=' + search_name + '&Location=' + search_town + '&x=38&y=13'
r = requests.get(query)
if r.status_code != 200:
	print RED + 'Whoops didnt get a response...' + END
else:
	print GREEN + 'HTTP Status Code is: ' + str(r.status_code) + END
	t = r.text
	for s in re.finditer(name_search,t):
		name = s.group(1)
		rec = name
		if rec not in name_res:
			name_res.append(rec)
	for s in re.finditer(phone_search,t):
		phone = s.group(1)
		rec = phone
		if rec not in phone_res:
			phone_res.append(rec)
	for s in re.finditer(address_search,t):
		address = s.group(1)
		rec = address
		if rec not in addr_res:
			addr_res.append(rec)

p = zip(name_res, phone_res, addr_res)
for x in p:
	print GREEN + 'Name: ' + END + x[0] + GREEN + ' Phone: ' + END + str(x[1]) + GREEN + ' Address: ' + END + x[2]