#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re
import sys

# Add some colouring for printing packets later
YELLOW = '\033[93m' # Yellow is for information
GREEN = '\033[92m' # Green is GOOD, means something worked
END = '\033[0m' # It's the end of the world as we know it
RED = '\033[91m' # Red is bad, means something didn't work

name_res = []
phone_res = []
addr_res = []
url = 'http://www.thephonebook.bt.com/publisha.content/en/search/residential/search.publisha?'

if len(sys.argv) != 3:
	print 'Usage is ./btphone [Surname] [Location]'
	print 'Example: ./btphone Bloggs Moon'
	sys.exit(1)

search_name = sys.argv[1]
search_town = sys.argv[2]

name_search = 'recordTitle">.(\S.*)</div>'
phone_search = 'class="phone">Tel:.(\S.*)</span>.-.<'
address_search = '<div>(\S.*).-.<a href="map'

query = url + 'Surname=' + search_name + '&Location=' + search_town + '&Initial=&Street='
print query
r = requests.get(query)
if r.status_code != 200:
	print RED + 'Whoops didnt get a response...' + END
else:
	data = r.text
	soup = BeautifulSoup(data)
	for link in soup.find_all('div',class_="recordTitle"):
		print link