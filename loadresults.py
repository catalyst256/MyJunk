#!/usr/bin/env python

# Script to load the results from onionrunner by Justin Seitz into ElasticSearch

import glob
from elasticsearch import Elasticsearch
import sys
import datetime
import json

# ElasticSearch options
server = 'skybox'
port = 9200
index = 'osint'
doctype = 'onion'


def sendtoelastic(data):
    try:
        es = Elasticsearch(server)
        data['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        es.index(index=index, doc_type=doctype, body=data)
    except Exception as e:
        print 'Error sending to elasticsearch: {0}'.format(str(e))
        pass


def main(path):
    files = glob.glob('{0}*.json'.format(path))
    print '[-] Loaded {0} files for import'.format(str(len(files)))
    for f in files:
        data = open(f, 'rb').read()
        scan_result = ur"%s" % data.decode("utf8")
        scan_result = json.loads(scan_result)
        sendtoelastic(scan_result)
        print '[*] Added {0} to ElasticSearch'.format(f)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: ./loadresults.py [results folder]'
        print 'Example: ./loadresults.py scan_results/'
        sys.exit(1)
    print '[!] Loading scan results from onionrunner....'
    main(sys.argv[1])
    print '[!] Results loaded: http://{0}:{1}/{2}/_search?q=*'.format(server, str(port), index)
