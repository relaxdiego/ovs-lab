import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from ovsdb_client import OVSDBClient

stamps = [
    {
        'name': 'Forever',
        'url': 'http://www.spellman.org/images/forever_stamp.jpg',
        'categories': [
            'historic'
        ]
    },

    {
        'name': 'Aborigine',
        'url': 'http://www.smh.com.au/ffxImage/'
               'urlpicture_id_1023864658551_2002/06/28/nat_stamp29.jpg',
        'categories': [
            'historic',
            'australia'
        ]
    },

    {
        'name': 'Amur Tiger Cub',
        'url': 'http://goodnature.nathab.com/'
               'wp-content/uploads/2011/10/Tiger-face1.png',
        'categories': [
            'animals'
        ]
    },

    {
        'name': 'Spiderman',
        'url': 'http://a.abcnews.go.com/images/Entertainment/'
               'ap_comicstamp_01_ssv.jpg',
        'categories': [
            'cartoons'
        ]
    },

    {
        'name': 'Homer Simpson',
        'url': 'http://s08214.biss.wikispaces.net/file/'
               'view/homer-stamp-14.jpg/125737775/homer-stamp-14.jpg',
        'categories': [
            'cartoons'
        ]
    }
]

operations = ['stamps']

for stamp in stamps:
    operations.append({
        'op': 'insert',
        'table': 'Stamp',
        'row': {
            'name': stamp['name'],
            'url': stamp['url'],
            'categories': [
                'set',
                stamp['categories']
            ]
        }
    })

client = OVSDBClient('localhost', 6640)

response = client.request({
    'id': 1,
    'method': 'transact',
    'params': operations
})


if response['error'] is None:
    print "Stamps database seeded"
else:
    print response
