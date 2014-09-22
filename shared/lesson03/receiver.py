import sys
from ovsdb_client import OVSDBClient

client = OVSDBClient(sys.argv[1], 6640)

print "Connecting to chat room..."

response = client.request({
    'id': 1,
    'method': 'monitor',
    'params': [
        'chat',
        1,
        {
            'Message': {}
        }
    ]
})

if response['error']:
    raise "Could not connect to chat room!"
else:
    print "Connected."

while True:
    # Check for messages from server
    message = None
    try:
        message = client.receive()
    except OVSDBClient.ReceiveTimeoutError:
        pass

    # Skip the rest if no message received
    if not message:
        continue

    # Respond to inactivity probe from OVSDB
    if message['method'] == 'echo':
        print "(OVSDB) PING?"
        client.send({
            'id': message['id'],
            'error': None,
            'result': message['params']
        })
        print "PONG!"

    # Extract message from update notification
    if message['method'] == 'update':
        row = message['params'][1]['Message'].values()[0]['new']
        print "({}) {}".format(row['sender'], row['message'])
