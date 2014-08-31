#!/usr/bin/python

from common import createTopology


createTopology(
    's2',
    [
        [
            'red2',
            {
                'ip': '10.0.0.2/8',
                'mac': '00:00:00:00:aa:02'
            }
        ],
        [
            'blue2',
            {
                'ip': '10.0.0.2/8',
                'mac': '00:00:00:00:aa:02'
            }
        ]
    ]
)
