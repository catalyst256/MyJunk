#!/usr/bin/env python3

# Author: Adam Maxwell (@catalyst256)
# Simple script to get associated email addresses from a PGP signature block

# Used https://cirw.in/gpg-decoder to work out the correct offsets to pull for the keyid


import sys
import base64
import re
import binascii
import requests
import validators


regex_pgp = re.compile(
    r"-----BEGIN [^-]+-----([A-Za-z0-9+\/=\s]+)-----END [^-]+-----", re.MULTILINE)

regex_email = re.compile(r'([\w.-]+@[\w.-]+\.\w+)', re.MULTILINE)


def check_keyid(keyid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    server = 'http://keys.gnupg.net/pks/lookup?search=0x{0}&fingerprint=on&op=index'.format(
        keyid)
    resp = requests.get(server, headers=headers)
    # If the response is valid use regex to pull out any email addresses
    print('[-] We got a {0} response...'.format(resp.status_code))
    if resp.status_code == 200:
        email = re.findall(regex_email, resp.text)
        return email
    else:
        print('[!] Whoops, we got a {0}'.format(resp.status_code))
        return None


def main(filename):
    m = open(filename, 'r').read()
    # Find the PGP Signature block, removing the start and end
    matches = regex_pgp.findall(m)[0]
    # Base64 decode the signature block
    b64 = base64.b64decode(matches)
    # Convert the base64 to hex
    hx = binascii.hexlify(b64)
    # Get the offsets for the Key ID
    keyid = hx.decode()[48:64]
    print('[+] Found Key ID: {}'.format(keyid))
    # Check the Key ID against the PGP key servers
    print('[!] Checking PGP Key Server...')
    emails = check_keyid(keyid)
    print('[+] Found {0} emails...'.format(len(emails)))
    if emails:
        for email in emails:
            print('[-] Found: {0}'.format(email))


if __name__ == '__main__':
    main(sys.argv[1])
