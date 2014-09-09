#!/usr/bin/python

from common import createTopology


createTopology(
    's1',
    [
        [
            'red1',
            {
                'ip': '10.0.0.1/8',
                'mac': '00:00:00:00:aa:01'
            }
        ],
        [
            'blue1',
            {
                'ip': '10.0.0.1/8',
                'mac': '00:00:00:00:aa:01'
            }
        ]
    ]
)
