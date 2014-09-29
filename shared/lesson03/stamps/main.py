#!/usr/bin/python

import os
import sys

from flask import Flask, render_template, request

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from ovsdb_client import OVSDBClient

app = Flask(__name__)


@app.route('/')
def index():
    client = OVSDBClient('localhost', 6640)

    query = {
        'id': 1,
        'method': 'transact',
        'params': [
            'stamps',
            {
                'op': 'select',
                'table': 'Stamp',
                'where': []
            }
        ]
    }

    response = client.request(query)
    return render_template('index.html', stamps=response['result'][0]['rows'])


@app.route('/view')
def view():
    client = OVSDBClient('localhost', 6640)

    query = {
        'id': 2,
        'method': 'transact',
        'params': [
            'stamps',
            {
                'op': 'select',
                'table': 'Stamp',
                'where': [
                    ['_uuid', '==', ['uuid', request.args.get('id')]]
                ]
            }
        ]
    }

    response = client.request(query)
    return render_template('view.html', stamp=response['result'][0]['rows'][0])


if __name__ == "__main__":
    app.debug = True
    app.run(host='192.168.101.10', port=8080)
