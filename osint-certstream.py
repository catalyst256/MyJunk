#!/usr/bin/env python3

# Original code for this was taken from https://github.com/CaliDog/certstream-python

# To run this requires you to do "pip3 install certstream" firsts

import logging
import sys
import datetime
import certstream
import argparse


keywords = []
logging.basicConfig(
    format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)


def load_keywords(filename):
    keywords_file = open(filename, 'r').readlines()
    for keyword in keywords_file:
        keywords.append(keyword.strip('\n'))


def certstream_callback(message, context):
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        domains = message['data']['leaf_cert']['all_domains']
        domain = domains[0]
        if [k for k in keywords if k in ' '.join(domains)]:
            sys.stdout.write(u"[{}] {} {} \n".format(datetime.datetime.now().strftime(
                '%m/%d/%y %H:%M:%S'), domain, ','.join(domains)))
            sys.stdout.flush()


def main(filename):
    load_keywords(filename)
    print('[+] Found {0} keywords to use..'.format(len(keywords)))
    print('[+] Searching Certstream for {0}..'.format(','.join(keywords)))
    certstream.listen_for_events(
        certstream_callback, url='wss://certstream.calidog.io/')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
