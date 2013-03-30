import os
from optparse import OptionParser

import requests
from flask import Flask, make_response, request
app = Flask("Daydreams")


@app.route('/fetch', methods=['POST'])
def fetch():
    url = request.form.get('url')
    return requests.get(url).text


@app.route('/codeburn/')
def burn():
    with open('codeburn/index.html') as f:
        return f.read()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.endswith('.py'):
        return make_response('Cannot serve PY files', 400)
    if not os.path.exists(path):
        return make_response('Not found', 404)
    with open(path) as f:
        return f.read()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--port', dest='port',
            help='port', metavar='PORT', default=os.getenv('PORT', '8000'))
    parser.add_option('--host', dest='hostname',
            help='hostname', metavar='HOSTNAME', default='0.0.0.0')
    (options, args) = parser.parse_args()
    app.debug = True
    app.run(host=options.hostname, port=int(options.port))
