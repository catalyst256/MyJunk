#!/usr/bin/env python

import json, subprocess
from flask import Flask, request, jsonify, make_response


app = Flask(__name__)


def queryDomain(domain):
    a = subprocess.run(["/bin/pwhois","--json","%s"%domain],capture_output=True).stdout
    j = json.loads(a)
    return j


@app.route('/query/', methods=['GET'])
def lookupDomain():
    domain = request.args.get('domain')
    x = queryDomain(domain)
    return make_response(jsonify({'Query': x}))


if __name__ == '__main__':
    app.run(port=9119, debug=True)
