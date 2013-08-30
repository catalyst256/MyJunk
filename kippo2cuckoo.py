#!/usr/bin/env python
 
# Simple script to submit files from Kippo Honeypot to a Cuckoo Sandbox via the Cuckoo API
# Created by @catalyst256
 
import requests, glob, os
 
# User defined settings - change these if they are different for your setup
sandbox_ip = '127.0.0.1' # Define the IP for the Cuckoo sandbox API
sandbox_port = '8090' # Here if you need to change the port that the Cuckoo API runs on
kip_dl = '/var/kippo/dl/' # Kippo dl file location - make sure to include trailing /
file_history = 'history.txt' # Keeps a history of files submitted to Cuckoo
log_file = 'output-log.txt' # Log file for storing a list of submitted files and the task ID from Cuckoo

file_list = [] # List of files already in Kippo
file_new = [] # List of new files to submit to Cuckoo

def load_existing(file_history):

	if not os.path.exists(file_history):
		file(file_history, 'w').close()

	with open(file_history) as f_in:
		lines = (line.rstrip() for line in f_in)		
		lines = (line for line in lines if line)
		for i in lines:
			if i not in file_list:
				file_list.append(i)

	files = glob.glob(kip_dl + '*')
	for s in files:
		if s not in file_list:
			file_new.append(s)

	f = open(file_history, 'a')
	for t in file_new:
		f.writelines(str(t)+'\n')
	f.close()

 
def sandbox_submit(files): # Function to submit the files to cuckoo using the REST API
	sandbox_url = 'http://' + sandbox_ip + ':' + sandbox_port + '/tasks/create/file' # create the URL to POST files to
	print sandbox_url
	try:
		files = {'file': open(files, 'rb')}
		s = requests.post(sandbox_url, files=files)
		print s.status_code
		print s.text
	except:
		print 'Error has occurred'

load_existing(file_history)
for files in file_new:
	print files
	sandbox_submit(files)
 