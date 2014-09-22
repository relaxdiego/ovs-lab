import sys
from ovsdb_client import OVSDBClient

nickname = sys.argv[2]
message_id = 0

while True:
    message = raw_input('Your message: ')

    client = OVSDBClient(sys.argv[1], 6640)
    message_id += 1

    response = client.request({
        'id': message_id,
        'method': 'transact',
        'params': [
            'chat',
            {
                'op': 'insert',
                'table': 'Message',
                'row': {
                    'sender': nickname,
                    'message': message
                }
            }
        ]
    })

    if response and response['error']:
        raise "Could not send message!"
